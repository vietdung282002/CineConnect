# Generated by Django 5.0.4 on 2024-05-18 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0037_movie_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='rate_avr',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='rate_count',
            field=models.BigIntegerField(default=0),
        ),
    ]