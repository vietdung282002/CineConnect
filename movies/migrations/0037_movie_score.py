# Generated by Django 5.0.4 on 2024-05-18 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0036_alter_movie_backdrop_path_alter_movie_poster_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='score',
            field=models.FloatField(default=0),
        ),
    ]
