from .models import User, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(signal=post_save, sender=User)
def create_profile_post_user_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)