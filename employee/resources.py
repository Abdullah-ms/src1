from import_export import resources
from .models import Employee
from datetime import datetime


class EmployeeResource(resources.ModelResource):

    def dehydrate_created_at(self, employee):
        # إزالة التوقيت الزمني من created_at
        if employee.created_at:
            return employee.created_at.replace(tzinfo=None)
        return employee.created_at

    def dehydrate_updated_at(self, employee):
        # إزالة التوقيت الزمني من updated_at إذا كان موجودًا
        if employee.updated_at:
            return employee.updated_at.replace(tzinfo=None)
        return employee.updated_at

    class Meta:
        model = Employee
