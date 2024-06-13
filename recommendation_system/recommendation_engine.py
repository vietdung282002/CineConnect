import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movies.models import Movie
from watched.models import Watched
from favourite.models import Favourite
from asgiref.sync import sync_to_async
from .models import TfidfMatrixModel,CosineModel, MovieRecommend

import logging

logger = logging.getLogger(__name__)


    
def create_tfidf_matrix():
    movies = Movie.objects.values('overview')
    df_movielens = pd.DataFrame(list(movies))

    tfidfv = TfidfVectorizer(analyzer='word', stop_words='english')

    tfidfv_matrix = tfidfv.fit_transform(df_movielens['overview'])
 
    tfidfv_dense = tfidfv_matrix.todense()
    
    entries = TfidfMatrixModel.objects.all()
    entries.delete()
    
    matrix_model = TfidfMatrixModel()
    matrix_model.save_matrix(tfidfv_matrix)
    # logger.warning(matrix_model.get_matrix())
    # logger.warning(tfidfv_matrix)
    return tfidfv_matrix
    
    
def cal_cosine_simulator():
    tfidfv_matrix = create_tfidf_matrix()
    cosine_sim = linear_kernel(tfidfv_matrix, tfidfv_matrix)
    entries = CosineModel.objects.all()
    entries.delete()
    cosine_model = CosineModel()
    cosine_model.save_matrix(cosine_sim)
    # logger.warning(cosine_sim.shape)
    # logger.warning(cosine_model.get_matrix)
    
def content_recommendations(movie,user):
    cosine_sim_model = CosineModel.objects.first()
    cosine_sim_matrix = cosine_sim_model.get_matrix()
    movies = Movie.objects.all().values('id','title')
    df_movielens = pd.DataFrame(list(movies))
    indices = pd.Series(df_movielens.index, index=df_movielens['title']).drop_duplicates()

    idx = indices[movie.title]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    
    sim_scores.sort(key=lambda x: x[1].any(), reverse=True)
    
    # sim_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in sim_scores]
    
    recommended_movies = df_movielens['id'].iloc[movie_indices].tolist()
    watched_query = Watched.objects.filter(user=user)
    favourite_query = Favourite.objects.filter(user=user)
    watched_list = []
    for watched in watched_query:
        watched_list.append(watched.movie.id)
    
    for favourite in favourite_query:
        watched_list.append(favourite.movie.id)
    logger.warning(recommended_movies)
    
    if MovieRecommend.objects.filter(movie=movie,user = user).exists():
        MovieRecommend.objects.get(movie=movie,user = user).delete()
    
    i=0
    for movie_id in recommended_movies:
        if movie_id in watched_list :
            continue
        
        if i>10:
            break
        else: i+=1
        movie_recommend = MovieRecommend.objects.get_or_create(user=user,movie_id=movie_id)