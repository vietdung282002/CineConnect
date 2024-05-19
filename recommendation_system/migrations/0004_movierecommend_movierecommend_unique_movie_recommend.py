# Generated by Django 5.0.4 on 2024-05-19 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0039_remove_movie_score'),
        ('recommendation_system', '0003_rename_cosine_model_cosinemodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieRecommend',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('movie_base_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_base_on', to='movies.movie')),
                ('movie_recommend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_recommend', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='movierecommend',
            constraint=models.UniqueConstraint(fields=('movie_recommend', 'movie_base_on'), name='unique_movie_recommend'),
        ),
    ]
