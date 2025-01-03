from django import forms
from django.contrib.auth.forms import UserCreationForm
from Main.models import CustomUser
from django.forms import ModelForm
# Corrected import of BusRoute from the 'bus' app
from bus.models import BusRoute
from train.models import TrainRoute# Ensure this is correct path to your BusRoute model
from air.models import AirRoute
from launch.models import LaunchRoute

# EmployeeSignupForm to handle employee registration
class EmployeeSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=15)
    employee_id = forms.CharField(required=True, max_length=20)
    designation = forms.CharField(required=True, max_length=100)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'employee_id', 'designation', 'password1', 'password2']

# BusRoutesForm to manage BusRoute creation
class BusRoutesForm(ModelForm):
    class Meta:
        model = BusRoute
        fields = '__all__'  # This will include all fields from BusRoute model

class TrainRouteForm(ModelForm):
    class Meta:
        model = TrainRoute
        fields = '__all__'
class AirRouteForm(ModelForm):
    class Meta:
        model = AirRoute
        fields = '__all__'
class LaunchRouteForm(ModelForm):
    class Meta:
        model = LaunchRoute
        fields = '__all__'