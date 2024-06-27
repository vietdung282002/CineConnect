from django.contrib import admin
from .models import TfidfMatrixModel,MovieRecommend,CosineModel,CountVectorizerModel
# Register your models here.
admin.site.register(TfidfMatrixModel)
admin.site.register(MovieRecommend)
admin.site.register(CosineModel)
admin.site.register(CountVectorizerModel)

