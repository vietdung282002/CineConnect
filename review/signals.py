from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Reaction

@receiver(post_save, sender=Reaction)
def send_reaction_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "reactions_group",
        {
            'type': 'reaction_message',
            'review_id': instance.review.id,
            'like': instance.like,
            'dislike': instance.dislike
        }
    )