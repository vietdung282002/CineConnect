from django.shortcuts import render
from rest_framework import viewsets,mixins
from .serializers import TestSerializers,TestWJob

from django.http import HttpResponse

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .tasks import my_task
# Create your views here.
class TestViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = TestWJob.objects.all()
    serializer_class = TestSerializers
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
def index(request):
    my_task.delay()
    return HttpResponse("Task Started!")

def schedule_task(request):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.get_or_create(
        interval=interval,
        name="my-schedule",
        task="webjob.tasks.my_task",
        #args=json.dumps(["Arg1", "Arg2"])
        #one_off=True
    )

    return HttpResponse("Task scheduled!")