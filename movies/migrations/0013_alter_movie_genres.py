# Generated by Django 5.0.4 on 2024-04-30 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genres', '0002_rename_genrers_genre'),
        ('movies', '0012_alter_movie_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='genres.genre'),
        ),
    ]
