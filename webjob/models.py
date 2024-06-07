from django.db import models

# Create your models here.
class TestWJob(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    time_stamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.time_stamp)