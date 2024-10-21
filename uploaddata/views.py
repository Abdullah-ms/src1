from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps
from .forms import UploadFileForm
import pandas as pd
import traceback
from django.db import models, IntegrityError, transaction
from django.utils import timezone
from django.utils.timezone import is_naive
from django.views.decorators.csrf import csrf_protect
import re


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Read the file without parsing dates
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, parse_dates=False)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file, parse_dates=False)
                else:
                    messages.error(request, 'Unsupported file format.')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                # Clean the column headers
                df.columns = df.columns.str.strip().str.strip('#').str.strip(' #').str.strip('# ').str.replace(' ',
                                                                                                               '_').str.lower()

                # Drop 'id' column if it exists
                if 'id' in df.columns:
                    df = df.drop(columns=['id'])

                # Convert NaN values to None for all columns
                df = df.where(pd.notnull(df), None)

                # Log the cleaned DataFrame columns
                print(f'Cleaned DataFrame columns: {df.columns.tolist()}')

                # Get all models in all apps
                app_models = apps.get_models()

                # Find the model that matches the columns
                target_model = None
                for model in app_models:
                    model_fields = set(field.name for field in model._meta.fields)
                    if set(df.columns).issubset(model_fields):
                        target_model = model
                        break

                # Log the model fields found
                if target_model:
                    print(f'Matching model found: {target_model.__name__}')
                    print(f'Model fields: {model_fields}')
                else:
                    print('No matching model found for the provided data.')

                if not target_model:
                    messages.error(request, 'No matching model found for the provided data.')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                # Identify unique fields (excluding auto-incremented primary key)
                unique_fields = []
                for field in target_model._meta.fields:
                    if field.primary_key:
                        if isinstance(field, models.AutoField):
                            # Skip auto-incremented primary key
                            continue
                        else:
                            unique_fields.append(field.name)
                    elif field.unique:
                        unique_fields.append(field.name)

                # If unique_together is used
                if hasattr(target_model._meta, 'unique_together'):
                    for unique_group in target_model._meta.unique_together:
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

                # Remove duplicates based on unique fields
                df = df.drop_duplicates(subset=unique_fields)

                # Identify DateTimeFields in the model
                datetime_fields = [
                    field.name for field in target_model._meta.fields
                    if isinstance(field, models.DateTimeField)
                ]

                # Parse datetime fields and make them time zone–aware
                for datetime_field in datetime_fields:
                    if datetime_field in df.columns:
                        # Parse dates without specifying format
                        df[datetime_field] = pd.to_datetime(df[datetime_field], errors='coerce')

                        # Handle unparsed dates with specific formats
                        unparsed_dates = df[datetime_field].isnull()
                        if unparsed_dates.any():
                            # Try alternative format with seconds
                            df.loc[unparsed_dates, datetime_field] = pd.to_datetime(
                                df.loc[unparsed_dates, datetime_field],
                                format='%d/%m/%Y %H:%M:%S',
                                errors='coerce'
                            )
                            # Update unparsed_dates
                            unparsed_dates = df[datetime_field].isnull()
                            if unparsed_dates.any():
                                # Try alternative format without seconds
                                df.loc[unparsed_dates, datetime_field] = pd.to_datetime(
                                    df.loc[unparsed_dates, datetime_field],
                                    format='%d/%m/%Y %H:%M',
                                    errors='coerce'
                                )

                        # After parsing attempts, check if any dates are still unparsed
                        if df[datetime_field].isnull().any():
                            invalid_dates = df[df[datetime_field].isnull()][datetime_field]
                            messages.error(
                                request,
                                f'The following datetime values in the "{datetime_field}" column could not be parsed: '
                                f'{", ".join(invalid_dates.astype(str).unique())}. '
                                f'Please ensure they are in one of the accepted formats.'
                            )
                            return render(request, 'uploaddata/upload.html', {'form': form})

                        # Make datetime objects time zone–aware
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
                        # Convert column to numeric and handle errors
                        df[int_field] = pd.to_numeric(df[int_field], errors='coerce').astype('Int64')

                # Handle ForeignKey fields
                foreign_key_fields = [
                    field for field in target_model._meta.fields
                    if isinstance(field, models.ForeignKey)
                ]
                for fk_field in foreign_key_fields:
                    fk_name = fk_field.name
                    related_model = fk_field.related_model
                    if fk_name in df.columns:
                        # Replace foreign key values with related model instances
                        def get_related_instance(value):
                            if pd.notnull(value):
                                if re.match(r'^\d+$', str(value)):
                                    try:
                                        return related_model.objects.get(pk=value)
                                    except related_model.DoesNotExist:
                                        print(f'Invalid ForeignKey value "{value}" for field "{fk_name}".')
                                        return None
                                else:
                                    # Try to lookup by a slug or name field if primary key is not numeric
                                    lookup_fields = ['slug', 'name']
                                    for field in lookup_fields:
                                        if hasattr(related_model, field):
                                            try:
                                                return related_model.objects.get(**{field: value})
                                            except related_model.DoesNotExist:
                                                continue
                                    print(
                                        f'Invalid ForeignKey value "{value}" for field "{fk_name}" after attempting lookup by slug or name.')
                                    return None
                            print(f'Non-numeric ForeignKey value "{value}" for field "{fk_name}".')
                            return None

                        df[fk_name] = df[fk_name].apply(get_related_instance)

                        # Log if there are any None values that could cause issues
                        if df[fk_name].isnull().any():
                            messages.error(
                                request,
                                f'ForeignKey field "{fk_name}" has invalid values that could not be resolved. Please check the data and try again.'
                            )
                            return render(request, 'uploaddata/upload.html', {'form': form})

                # Log the processed DataFrame
                print(f'Processed DataFrame:\n{df.head()}')
                print(f'DataFrame shape: {df.shape}')

                # Replace pd.NA with None
                df = df.replace({pd.NA: None})

                # Ensure 'id' field is not passed to the model
                if 'id' in df.columns:
                    df = df.drop(columns=['id'])

                # Batch create records in bulk
                records = [target_model(**row.to_dict()) for _, row in df.iterrows()]
                if not records:
                    messages.error(request, 'No valid records to upload after processing the file.')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                batch_size = 1000  # Define your batch size
                try:
                    with transaction.atomic():
                        for i in range(0, len(records), batch_size):
                            created_records = target_model.objects.bulk_create(records[i:i + batch_size],
                                                                               ignore_conflicts=True)
                            print(f'Inserted {len(created_records)} records out of {len(records)}')
                except IntegrityError as e:
                    messages.error(request, f'Error during bulk create: {e}')
                    return render(request, 'uploaddata/upload.html', {'form': form})

                messages.success(request, 'File uploaded successfully.')
                return redirect('upload_file')
            except IntegrityError as e:
                # Handle duplicate entries
                messages.error(request, f'Duplicate entry error: {e}')
                return render(request, 'uploaddata/upload.html', {'form': form})
            except Exception as e:
                traceback_str = traceback.format_exc()
                messages.error(request, f'Error processing file: {e}')
                print(traceback_str)  # For debugging purposes
                return render(request, 'uploaddata/upload.html', {'form': form})
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors and try again.')
            return render(request, 'uploaddata/upload.html', {'form': form})
    else:
        # Handle GET request
        form = UploadFileForm()
        return render(request, 'uploaddata/upload.html', {'form': form})
