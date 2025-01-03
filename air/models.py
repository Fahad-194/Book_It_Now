from django.db import models
from django.utils import timezone


class AirRoute(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()

    economy_class = models.IntegerField(default=0)
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)

    business_class = models.IntegerField(default=0)
    business_price = models.DecimalField(max_digits=10, decimal_places=2)

    first_class = models.IntegerField(default=0)
    general_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class AirBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    route = models.ForeignKey('AirRoute', on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=50)
    seats_reserved = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='booked')  # Add a status field
    def __str__(self):
        return f'Booking by {self.name} for {self.route}'









