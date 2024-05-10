# Generated by Django 5.0.4 on 2024-05-10 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0035_rename_charactor_cast_character'),
        ('watched', '0002_delete_watched'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Watched',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time_stamp',),
            },
        ),
        migrations.AddConstraint(
            model_name='watched',
            constraint=models.UniqueConstraint(fields=('user', 'movie'), name='unique_movie_user_watched'),
        ),
    ]
