from django.db import models

# Create your models here.
class Test(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    time_stamp = models.DateTimeField(auto_now=True)


