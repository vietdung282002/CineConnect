from rest_framework import status
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from favourite.models import Favourite
from rating.models import Rating
from review.models import Review
from movies.models import Movie
from users.models import CustomUser
from .serializers import FavouriteSerializers, FavouriteDetailSerializers
import threading
from recommendation_system import recommendation_engine
from rest_framework.decorators import action

# Create your views here.
class FavouriteViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
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
            return Response({'message': 'Object already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            favourite = Favourite.objects.create(movie=movie, user=user)
            data = {
                "status": "success",
                "message": FavouriteSerializers(favourite).data
            }
            thread = threading.Thread(target=recommendation_engine.content_recommendations(movie=movie,user=user))
            thread.start()
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        try:
            favourite_obj = Favourite.objects.get(user_id=request.user.id, movie_id=pk)
            try:
                rating_obj = Rating.objects.get(user_id=request.user.id, movie_id=pk)
                return Response({'error': "You can't not remove from watched because there is activity on it"},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
            except Rating.DoesNotExist:
                try:
                    review_obj = Review.objects.get(user_id=request.user.id, movie_id=pk)
                    return Response({'error': "You can't not remove from watched because there is activity on it"},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)
                except Review.DoesNotExist:
                    favourite_obj.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
        except Favourite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    # @action(detail=False, methods=['get'])  
    # def movie(self, request, *args, **kwargs):
    #     query = request.query_params.get('movie', None)
    #     if query:
    #         movie =Movie.objects.get(id = query)
    #         favourite = Favourite.objects.filter(movie = movie)
            
    #     return super().list(request, *args, **kwargs)