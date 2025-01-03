from django.db.models.signals import post_save
from django.dispatch import receiver
from Main.models import CustomUser  # Import the CustomUser from Main app
from .models import UserProfile  # Import UserProfile from prof app

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
