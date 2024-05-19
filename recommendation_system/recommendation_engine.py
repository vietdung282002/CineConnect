import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movies.models import Movie
import asyncio
from asgiref.sync import sync_to_async
from .models import TfidfMatrixModel

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

    retrieved_matrix = matrix_model.get_matrix()
    logger.warning((tfidfv_matrix != retrieved_matrix).nnz == 0)

async def run_async_task():
    await sync_to_async(create_tfidf_matrix)()

