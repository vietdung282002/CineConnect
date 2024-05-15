from django.db import models
from users.models import CustomUser
# Create your models here.
class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='follower')
    followee = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='followee')
    
    def __str__(self):
        return self.follower.username + " follow " +self.followee.username
    