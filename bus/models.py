from django.db import models

# Create your models here.
class BusRoute(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='reserved')  # 'reserved', 'paid', 'canceled'

    def __str__(self):
        return f"Booking for {self.customer_name} on {self.route}"