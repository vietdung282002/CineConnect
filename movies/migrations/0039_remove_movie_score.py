# Generated by Django 5.0.4 on 2024-05-19 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0038_movie_rate_avr_movie_rate_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='score',
        ),
    ]
