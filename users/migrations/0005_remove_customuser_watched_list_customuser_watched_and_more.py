# Generated by Django 5.0.4 on 2024-05-08 02:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0034_alter_cast_options_alter_movie_options'),
        ('users', '0004_watched_customuser_watched_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='watched_list',
        ),
        migrations.AddField(
            model_name='customuser',
            name='watched',
            field=models.ManyToManyField(related_name='user_watched', through='users.Watched', to='movies.movie'),
        ),
        migrations.AlterField(
            model_name='watched',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_list',
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
