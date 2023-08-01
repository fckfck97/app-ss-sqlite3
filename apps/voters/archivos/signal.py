from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

@receiver(post_save, sender=SocialAccount)
def user_created(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.is_active = False
        user.save()