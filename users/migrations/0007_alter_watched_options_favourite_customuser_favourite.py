# Generated by Django 5.0.4 on 2024-05-08 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0034_alter_cast_options_alter_movie_options'),
        ('users', '0006_alter_customuser_options_watched_time_stamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watched',
            options={'ordering': ('time_stamp',)},
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_movie',
                                            to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_list',
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('time_stamp',),
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='favourite',
            field=models.ManyToManyField(related_name='user_favourite', through='users.Favourite', to='movies.movie'),
        ),
    ]
