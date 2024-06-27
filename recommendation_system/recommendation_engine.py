import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movies.models import Movie,Person
from genres.models import Genre
from watched.models import Watched
from favourite.models import Favourite
from asgiref.sync import sync_to_async
from .models import TfidfMatrixModel,CosineModel,CountVectorizerModel, MovieRecommend
from django.db.models import Prefetch
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
    return tfidfv_matrix

def createCountVectorizer():
    movies = Movie.objects.prefetch_related('casts__person', 'directors__person', 'genres').all()

    data = []
    for movie in movies:
        actors = [cast.cast.name for cast in movie.cast.all()[:3]]
        directors = [director.director.name for director in movie.director.all()]
        genres = [genre.name for genre in movie.genres.all()[:3]]

        data.append({
            'title': movie.title,
            'actors': actors,
            'director': ', '.join(directors),
            'genres': genres,
        })

    df_movies = pd.DataFrame(data)
    df_movies['director']=df_movies['director'].apply(lambda x: clean_director(x))
    df_movies['actor']=df_movies['actors'].apply(lambda x:clean_top3(x))
    df_movies['genres']=df_movies['genres'].apply(lambda x:clean_top3(x))
    df_movies['soup'] = df_movies.apply(create_soup, axis=1)
    cv = CountVectorizer(stop_words='english')
    cv_matrix = cv.fit_transform(df_movies['soup'])
    cv_matrix = cv_matrix.todense()
    
    cv_matrix = np.asarray(cv_matrix)
    entries = CountVectorizerModel.objects.all()
    entries.delete()
    
    matrix_model = CountVectorizerModel()
    matrix_model.save_matrix(cv_matrix)
    return cv_matrix
    

def create_soup(x):
    return  ' '.join(x['actor']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
    
def clean_director(x):
    return x.lower().replace(' ','')

def clean_top3(x):
    new=[]
    for a in x:
        new.append(a.lower().replace(' ',''))
    return new
    
def cal_cosine_simulator():
    tfidfv_matrix = create_tfidf_matrix()
    cosine_sim = linear_kernel(tfidfv_matrix, tfidfv_matrix)
    entries = CosineModel.objects.all()
    entries.delete()
    cosine_model = CosineModel()
    cosine_model.save_matrix(cosine_sim)
    
    countVectorizer = createCountVectorizer()
    cosine_sim =  cosine_similarity(countVectorizer, countVectorizer)
    cosine_model2 = CosineModel()
    cosine_model2.save_matrix(cosine_sim)

    
def content_recommendations(movie,user):
    cosine_sim = CosineModel.objects.all()
    list_A = []
    list_B = []
    recommended_movies = []
    first_iteration = True
    for cosine_sim_model in cosine_sim:
        cosine_sim_matrix = cosine_sim_model.get_matrix()
        movies = Movie.objects.all().values('id','title')
        df_movielens = pd.DataFrame(list(movies))
        indices = pd.Series(df_movielens.index, index=df_movielens['title']).drop_duplicates()
        idx = indices[movie.title]
        sim_scores = list(enumerate(cosine_sim_matrix[idx]))
        sim_scores.sort(key=lambda x: x[1].any(), reverse=True)
        movie_indices = [i[0] for i in sim_scores]
        if first_iteration:
            list_A = df_movielens['id'].iloc[movie_indices].tolist()
            first_iteration = False
        else:
            list_B = df_movielens['id'].iloc[movie_indices].tolist()
            
    for a, b in zip(list_A, list_B):
        recommended_movies.append(a)
        recommended_movies.append(b)
    watched_query = Watched.objects.filter(user=user)
    favourite_query = Favourite.objects.filter(user=user)
    watched_list = []
    for watched in watched_query:
        watched_list.append(watched.movie.id)
    
    for favourite in favourite_query:
        watched_list.append(favourite.movie.id)
    
    if MovieRecommend.objects.filter(movie=movie,user = user).exists():
        MovieRecommend.objects.get(movie=movie,user = user).delete()
    
    i=0
    for movie_id in recommended_movies:
        if movie_id in watched_list :
            continue
        
        if i>10:
            break
        else: 
            i+=1
        movie_recommend = MovieRecommend.objects.get_or_create(user=user,movie_id=movie_id)