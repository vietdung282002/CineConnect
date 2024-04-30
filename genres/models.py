from django.db import models

# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(null=False,blank=False,max_length=50)
    
    def __str__(self):
        return self.name
    