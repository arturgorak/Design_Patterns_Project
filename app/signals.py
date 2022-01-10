from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Session


# @receiver(post_save, sender=Session)
# def current_session_signal(sender, created, instance, *args, **kwargs):
#     if instance.is_current_session is True:
#         Session.objects.exclude(pk=instance.id).update(is_current_session=False)
