from rest_framework import status
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from favourite.models import Favourite
from rating.models import Rating
from review.models import Review
from movies.models import Movie
from watched.models import Watched
from users.models import CustomUser
from .serializers import FavouriteSerializers, FavouriteDetailSerializers
import threading
from recommendation_system import recommendation_engine
from rest_framework.decorators import action
from activity.models import Activity
# Create your views here.
class FavouriteViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                    #    mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Favourite.objects.all()
    # permission_classes = [permissions.IsAuthenticated]

    # serializer_class = WatchedDetailSerializers
    def get_serializer_class(self):
        if self.action == 'list':
            return FavouriteDetailSerializers
        else:
            return FavouriteSerializers
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user.id

        return context

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('movie', None)
        try:
            query_set = Favourite.objects.filter(movie_id = query)
            self.queryset = query_set
            return super().list(request, *args, **kwargs)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = request.data
        movie_id = data.get('movie')
        movie = Movie.objects.get(id = movie_id)
        user = CustomUser.objects.get(id = request.user.id)
        if Favourite.objects.filter(user=user, movie=movie).exists():
            favourite = Favourite.objects.get(user=user, movie=movie)
            favourite.delete()
            data = {
                "status": "success",
                "message": {
                    "movie": movie_id,
                    "user": request.user.id,
                    "favourite": False
                }
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            try:
                watched = Watched.objects.get_or_create(user=user, movie=movie)
                favourite = Favourite.objects.create(movie=movie, user=user)
                activity = Activity.objects.create(movie=movie,user = user,type = 2)
                data = {
                    "status": "success",
                    "message": {
                        "movie": movie_id,
                        "user": request.user.id,
                        "favourite": True,
                        "watched":True
                    }
                }
                thread = threading.Thread(target=recommendation_engine.content_recommendations(movie,user))
                thread.start()
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                data = {
                    "status": "error",
                    "message": str(e)
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
