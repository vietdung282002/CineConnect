# Generated by Django 5.0.4 on 2024-05-10 07:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('movies', '0035_rename_charactor_cast_character'),
        ('review', '0005_remove_review_movie_remove_review_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_review',
                                            to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_review',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time_stamp',),
            },
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like_review',
                                           to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_review',
                                             to='review.review')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment_review',
                                   to=settings.AUTH_USER_MODEL)),
                ('review',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_related_review',
                                   to='review.review')),
            ],
            options={
                'ordering': ('time_stamp',),
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user', 'movie'), name='unique_movie_user_review'),
        ),
    ]
