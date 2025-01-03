from django.db import models
from django.utils import timezone


class LaunchRoute(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()

    cabin_class = models.IntegerField(default=0)
    cabin_price = models.DecimalField(max_digits=10, decimal_places=2)

    ac_chair_class = models.IntegerField(default=0)
    ac_chair_price = models.DecimalField(max_digits=10, decimal_places=2)

    chair_class = models.IntegerField(default=0)
    chair_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class LaunchBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    route = models.ForeignKey('LaunchRoute', on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=50)
    seats_reserved = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='booked')  # Add a status field
    def __str__(self):
        return f'Booking by {self.name} for {self.route}'









