from django import forms
from django.contrib.auth.models import User
from .models import TravelExperience
from Main.models import CustomUser
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','phone_number']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'full_name', 'address', 'phone_number', 'profession', 'journey_choice', 'bio']

class TravelExperienceForm(forms.ModelForm):
    class Meta:
        model = TravelExperience
        fields = ['title', 'description', 'photo', 'video']

