# Main/admin.py
from django.contrib import admin
from .models import CustomUser, UserActivity

# Register CustomUser model in the admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'employee_id', 'designation']
    search_fields = ['username', 'email']
    def get_queryset(self, request):
        return super().get_queryset(request).filter(employee_id__isnull=True)

# Register UserActivity model in the admin
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'user__email']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # You can filter by employee_id, using the related model field
        return queryset.filter(user__employee_id__isnull=True)
