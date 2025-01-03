from django.contrib import admin
from .models import AirRoute, AirBooking

# Register your models here.
admin.site.register(AirRoute)
admin.site.register(AirBooking)