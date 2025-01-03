from django.contrib import admin
from .models import BusRoute, Booking

# Register your models here.

admin.site.register(BusRoute)
admin.site.register(Booking)