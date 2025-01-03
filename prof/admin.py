from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = (
    'user', 'full_name', 'bio', 'phone_number', 'address', 'profession', 'journey_choice', 'profile_picture')

    # Fields to be used for searching in the admin
    search_fields = ('user__username', 'full_name', 'bio', 'phone_number', 'profession')

    # Add filters for fields like journey_choice
    list_filter = ('journey_choice', 'profession')

    # Make fields editable directly in the list view
    list_editable = ('full_name', 'bio', 'phone_number', 'address', 'profession', 'journey_choice')

    # Show inlines (if needed)
    # inlines = [CustomInline]


# Register UserProfile model with the admin
admin.site.register(UserProfile, UserProfileAdmin)
