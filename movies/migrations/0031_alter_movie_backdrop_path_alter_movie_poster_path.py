# Generated by Django 5.0.4 on 2024-05-03 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0030_director_movie_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='backdrop_path',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_path',
            field=models.CharField(null=True),
        ),
    ]
