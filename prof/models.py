from django.conf import settings
from django.db import models
from Main.models import CustomUser

class UserProfile(models.Model):
    JOURNEY_CHOICES = [
        ('Bus', 'Bus'),
        ('Air', 'Air'),
        ('Launch', 'Launch'),
        ('Train', 'Train'),
        # Add more choices as needed
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='prof_logo.jpg')
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    journey_choice = models.CharField(max_length=20, choices=JOURNEY_CHOICES, blank=True)

    def __str__(self):
        return self.user.username

class TravelExperience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="travel_experiences")
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='travel_photos/', blank=True, null=True)
    video = models.FileField(upload_to='travel_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.reactions.filter(reaction_type="like").count()

    @property
    def dislike_count(self):
        return self.reactions.filter(reaction_type="dislike").count()


class Reaction(models.Model):
    REACTION_CHOICES = [
        ("like", "Like"),
        ("dislike", "Dislike"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience = models.ForeignKey(TravelExperience, on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)

    def __str__(self):
        return f"{self.user} - {self.reaction_type} on {self.experience.title}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience = models.ForeignKey(TravelExperience, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.experience.title}"