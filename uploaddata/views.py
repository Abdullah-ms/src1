from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps
from .forms import UploadFileForm
import pandas as pd
from django.db import models, IntegrityError
from django.db.models import AutoField, DateTimeField
from django.utils import timezone
from django.utils.timezone import is_naive
from datetime import timedelta
import logging

# Initialize logger
logger = logging.getLogger(__name__)

# Function to convert 'HH:MM:SS' string into a timedelta object
def parse_duration(duration_str):
    if isinstance(duration_str, str) and duration_str.count(':') == 2:
        hours, minutes, seconds = map(int, duration_str.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    elif duration_str == '0':
        return timedelta(0)  # Allow '0' as a valid input for zero duration
    return None  # Allow None as a valid input for null duration

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Read the file with headers
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, header=0, parse_dates=False)  # Ensure headers are read
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file, header=0, parse_dates=False)  # Ensure headers are read
                else:
                    messages.error(request, 'Unsupported file format.')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                # Check if the DataFrame is empty
                if df.empty:
                    messages.error(request, 'The uploaded file is empty.')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                # Clean the column headers
                df.columns = df.columns.str.strip().str.strip('#').str.strip(' #').str.strip('# ').str.strip(' %') \
                    .str.replace('- ', '', regex=False).str.replace('(', '', regex=False).str.replace(')', '', regex=False) \
                    .str.replace('-', ' ', regex=False).str.replace(' ', '_', regex=False).str.lower()

                # Convert NaN values to None for all columns
                df = df.where(pd.notnull(df), None)

                # Process the 'duration' field
                if 'duration' in df.columns:
                    df['duration'] = df['duration'].apply(parse_duration)

                # Get all models from all installed apps
                app_models = apps.get_models()

                # Find the model that matches the columns
                target_model = None
                for model in app_models:
                    model_fields = set(field.name for field in model._meta.fields)
                    if set(df.columns).issubset(model_fields):
                        target_model = model
                        break

                if not target_model:
                    messages.error(request, 'No matching model found for the provided data.')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                # Identify unique fields (excluding auto-incremented primary key)
                unique_fields = []
                for field in target_model._meta.fields:
                    if field.primary_key:
                        if isinstance(field, AutoField):
                            continue  # Skip auto-incremented primary key
                        else:
                            unique_fields.append(field.name)
                    elif field.unique:
                        unique_fields.append(field.name)

                # If unique_together is used
                unique_together = getattr(target_model._meta, 'unique_together', ()) or ()
                if unique_together:
                    # Ensure unique_together is iterable
                    if isinstance(unique_together[0], str):
                        # If unique_together is defined as a single tuple of field names
                        unique_fields.extend(unique_together)
                    else:
                        for unique_group in unique_together:
                            unique_fields.extend(unique_group)

                unique_fields = list(set(unique_fields))  # Remove duplicates

                # Check if unique fields are present in DataFrame
                missing_fields = [field for field in unique_fields if field not in df.columns]
                if missing_fields:
                    messages.error(
                        request,
                        f'The following required fields are missing in the file: {", ".join(missing_fields)}'
                    )
                    return render(request, 'uploaddata/upload.html', {'form': form})

                # Remove duplicates based on unique fields in the DataFrame
                if unique_fields:
                    df = df.drop_duplicates(subset=unique_fields)

                # Remove records that already exist in the database
                if unique_fields:
                    # Fetch existing records from the database
                    existing_records = target_model.objects.all().values_list(*unique_fields)
                    existing_records_set = set(existing_records)

                    # Create a set of unique field tuples from the DataFrame
                    df['unique_tuple'] = df[unique_fields].apply(tuple, axis=1)
                    df = df[~df['unique_tuple'].isin(existing_records_set)]
                    df = df.drop(columns=['unique_tuple'])

                # Identify DateTimeFields in the model
                datetime_fields = [
                    field.name for field in target_model._meta.fields
                    if isinstance(field, DateTimeField)
                ]

                # Parse datetime fields and make them time zone–aware
                for datetime_field in datetime_fields:
                    if datetime_field in df.columns:
                        original_values = df[datetime_field].copy()
                        df[datetime_field] = pd.to_datetime(df[datetime_field], errors='coerce')

                        # Identify unparsed dates
                        unparsed_dates = df[datetime_field].isnull() & original_values.notnull()

                        if unparsed_dates.any():
                            df.loc[unparsed_dates, datetime_field] = pd.to_datetime(
                                original_values[unparsed_dates],
                                format='%d/%m/%Y %H:%M:%S',
                                errors='coerce'
                            )
                            unparsed_dates = df[datetime_field].isnull() & original_values.notnull()
                            if unparsed_dates.any():
                                df.loc[unparsed_dates, datetime_field] = pd.to_datetime(
                                    original_values[unparsed_dates],
                                    format='%d/%m/%Y %H:%M',
                                    errors='coerce'
                                )

                        if df[datetime_field].isnull().any():
                            invalid_dates = original_values[df[datetime_field].isnull()].unique()
                            messages.error(
                                request,
                                f'The following datetime values in the "{datetime_field}" column could not be parsed: '
                                f'{", ".join(map(str, invalid_dates))}. '
                                f'Please ensure they are in one of the accepted formats.'
                            )
                            return render(request, 'uploaddata/upload.html', {'form': form})

                        df[datetime_field] = df[datetime_field].apply(
                            lambda dt: timezone.make_aware(dt) if pd.notnull(dt) and is_naive(dt) else dt
                        )

                # Ensure integer fields have proper data types
                integer_fields = [
                    field.name for field in target_model._meta.fields
                    if isinstance(field, models.IntegerField)
                ]
                for int_field in integer_fields:
                    if int_field in df.columns:
                        df[int_field] = df[int_field].astype('Int64')

                # Replace pd.NA with None
                df = df.replace({pd.NA: None})

                # Identify ForeignKey fields in the model
                foreign_key_fields = {
                    field.name: field for field in target_model._meta.fields
                    if isinstance(field, models.ForeignKey)
                }

                # Pre-fetch related instances for ForeignKey fields
                related_instances = {}
                for field_name, field in foreign_key_fields.items():
                    related_model = field.related_model

                    # Identify all fields in the related model
                    related_model_fields = [f.name for f in related_model._meta.fields]

                    # Keep only the fields that are in the DataFrame
                    available_lookup_fields = [lf for lf in related_model_fields if lf in df.columns]

                    if not available_lookup_fields:
                        messages.error(
                            request,
                            f'Cannot find suitable lookup field for ForeignKey "{field_name}" in related model "{related_model.__name__}". '
                            f'Please ensure that one of the following fields is present in your data: {", ".join(related_model_fields)}.'
                        )
                        return render(request, 'uploaddata/upload.html', {'form': form})

                    # Use the first available lookup field
                    field_lookup = available_lookup_fields[0]

                    # Build a mapping from lookup field value to related instances
                    related_values = df[field_lookup].dropna().unique()
                    instances = related_model.objects.filter(**{f"{field_lookup}__in": related_values})

                    related_instances[field_name] = {}
                    for instance in instances:
                        key = getattr(instance, field_lookup)
                        if key in related_instances[field_name]:
                            related_instances[field_name][key].append(instance)
                        else:
                            related_instances[field_name][key] = [instance]

                # Batch processing: bulk create records in batches
                batch_size = 5000
                objects_to_create = []

                for _, row in df.iterrows():
                    row_dict = row.to_dict()
                    row_dict.pop('id', None)  # Remove the primary key if it's auto-incremented

                    # Handle ForeignKey fields
                    for field_name, field in foreign_key_fields.items():
                        if field_name in row_dict and row_dict[field_name] is not None:
                            # Identify the lookup field used
                            related_model_fields = [f.name for f in field.related_model._meta.fields]
                            available_lookup_fields = [lf for lf in related_model_fields if lf in row_dict]
                            if available_lookup_fields:
                                field_lookup = available_lookup_fields[0]
                            else:
                                messages.error(
                                    request,
                                    f'Cannot find suitable lookup field for ForeignKey "{field_name}" in related model "{field.related_model.__name__}". '
                                    f'Please ensure that one of the following fields is present in your data: {", ".join(related_model_fields)}.'
                                )
                                return render(request, 'uploaddata/upload.html', {'form': form})

                            related_value = row_dict[field_lookup]
                            instance_mapping = related_instances.get(field_name, {})
                            related_instances_list = instance_mapping.get(related_value)
                            if related_instances_list:
                                if len(related_instances_list) == 1:
                                    # Exactly one matching instance found
                                    row_dict[field_name] = related_instances_list[0]
                                else:
                                    messages.error(
                                        request,
                                        f'Multiple matching instances found for "{related_value}" in field "{field_name}". '
                                        f'Cannot resolve ForeignKey unambiguously.'
                                    )
                                    return render(request, 'uploaddata/upload.html', {'form': form})
                            else:
                                # Optionally create a new related instance
                                related_model = field.related_model
                                # Prepare default values for creating a new instance
                                create_kwargs = {field_lookup: related_value}
                                # You might need to handle other required fields here
                                new_instance = related_model.objects.create(**create_kwargs)
                                # Update the instance mapping
                                instance_mapping[related_value] = [new_instance]
                                related_instances[field_name][related_value] = [new_instance]
                                row_dict[field_name] = new_instance
                        elif field_name in row_dict:
                            row_dict[field_name] = None

                    objects_to_create.append(target_model(**row_dict))

                    if len(objects_to_create) >= batch_size:
                        target_model.objects.bulk_create(objects_to_create, ignore_conflicts=True)
                        objects_to_create = []

                # Insert any remaining objects
                if objects_to_create:
                    target_model.objects.bulk_create(objects_to_create, ignore_conflicts=True)

                messages.success(request, 'File uploaded successfully.')
                return redirect('upload_file')

            except IntegrityError as e:
                messages.error(request, f'Duplicate entry error: {e}')
                return render(request, 'uploaddata/upload.html', {'form': form})
            except Exception as e:
                logger.error('Error processing file', exc_info=True)
                messages.error(request, f'Error processing file: {e}')
                return render(request, 'uploaddata/upload.html', {'form': form})
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors and try again.')
            return render(request, 'uploaddata/upload.html', {'form': form})
    else:
        # Handle GET request
        form = UploadFileForm()
        return render(request, 'uploaddata/upload.html', {'form': form})
