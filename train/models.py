from django.db import models
from django.utils import timezone


class TrainRoute(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()

    ac_seats = models.PositiveIntegerField(default=0)
    ac_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    first_class_seats = models.PositiveIntegerField(default=0)
    first_class_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    shovan_chair_seats = models.PositiveIntegerField(default=0)
    shovan_chair_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    shovan_seats = models.PositiveIntegerField(default=0)
    shovan_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    shulov_seats = models.PositiveIntegerField(default=0)
    shulov_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.origin} to {self.destination}"


class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    route = models.ForeignKey('TrainRoute', on_delete=models.CASCADE)
    seat_class = models.CharField(max_length=50)
    seats_reserved = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='booked')  # Add a status field

    def __str__(self):
        return f'Booking by {self.name} for {self.route}'


