from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    Creates an Account associated with the newly created User instance 
    from Google OAuth.
    """
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    """
    Saves the Account instance when the User instance is saved.
    """
    try:
        instance.account.save()
    except Account.DoesNotExist:
        Account.objects.create(user=instance)
