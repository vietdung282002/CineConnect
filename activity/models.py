from django.db import models
from movies.models import Movie
from users.models import CustomUser
from review.models import Review
# Create your models here.
class Activity(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    type = models.IntegerField(null=False,blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_user')
    #type 1: User rervieww
    #type 2: User like movie
    #type 3: User Watched movie
    #type 4: User like review
    #type 5: User rate movie
    #type 6: User follow other user
    #type 7: User comment
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='activity_movie',null=True)
    user_follow = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_user',null=True)
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name="review_activity",null=True)
    time_stamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-time_stamp',)