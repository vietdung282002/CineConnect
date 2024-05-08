# Generated by Django 5.0.4 on 2024-05-05 14:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0034_alter_cast_options_alter_movie_options'),
        ('users', '0003_alter_customuser_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watched',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='watched_list',
            field=models.ManyToManyField(related_name='watched', through='users.Watched', to='movies.movie'),
        ),
    ]