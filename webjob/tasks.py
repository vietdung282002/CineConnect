from celery import shared_task
from .models import TestWJob

@shared_task
def test():
    object = TestWJob.objects.create()