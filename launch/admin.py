from django.contrib import admin
from .models import LaunchRoute, LaunchBooking

# Register your models here.
admin.site.register(LaunchRoute)
admin.site.register(LaunchBooking)