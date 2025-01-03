from django.db import models
from django.contrib.auth.models import AbstractUser

# Define the CustomUserManager class first
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def employees(self):
        # Filter users who are employees
        return self.filter(employee_id__isnull=False, designation__isnull=False)

    def normal_users(self):
        # Filter users who are not employees
        return self.filter(employee_id__isnull=True, designation__isnull=True)

    def get_by_natural_key(self, username):
        """
        This method is required when using a custom user manager.
        It allows Django to perform a lookup based on the natural key (usually 'username').
        """
        return self.get(username=username)

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and return a normal user with an email."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Use normalize_email from BaseUserManager
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser with an email."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


# Custom User model (handles both normal users and employees)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Optional for normal users
    designation = models.CharField(max_length=100, blank=True, null=True)  # Optional for normal users

    objects = CustomUserManager()  # Assign the custom manager here

    def is_employee(self):
        """Check if the user is an employee based on employee_id and designation."""
        return bool(self.employee_id and self.designation)

    def __str__(self):
        return self.username

# User Activity model (for all users, tracks signup/login)
class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('signup', 'Signup'),
        ('login', 'Login'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
