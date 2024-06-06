from celery import shared_task
from .models import Test

@shared_task
def create_new_object():
    # Logic để tạo một object mới
    new_object = Test.objects.create()
    new_object.save()