# employee/models.py
from django.db import models
from Main.models import CustomUser  # Import CustomUser from the Main app


# Proxy model for employees (inherits CustomUser but adds employee-specific filtering)
class Employee(CustomUser):
    class Meta:
        proxy = True  # This model does not create a new table
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.username


# EmployeeActivity model (tracks activities for employees only)
class EmployeeActivity(models.Model):
    ACTION_CHOICES = [
        ('signup', 'Signup'),
        ('login', 'Login'),
    ]
    # Use Employee model as the foreign key, assuming only employees should have this activity
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)  # Should link to Employee directly
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.action} - {self.timestamp}"
