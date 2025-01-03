# employee/admin.py
from django.contrib import admin
from .models import Employee, EmployeeActivity

# Register Employee model in the admin (show only employees)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'employee_id', 'designation']
    search_fields = ['username', 'email']

    # Apply filter to show only employees
    def get_queryset(self, request):
        return super().get_queryset(request).filter(employee_id__isnull=False, designation__isnull=False)

# Register EmployeeActivity model in the admin (track employee-specific activities)
@admin.register(EmployeeActivity)
class EmployeeActivityAdmin(admin.ModelAdmin):
    list_display = ['employee', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['employee__username', 'employee__email']

    def get_queryset(self, request):
        return super().get_queryset(request).filter(employee__employee_id__isnull=False,
                                                    employee__designation__isnull=False)