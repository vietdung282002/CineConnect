# Generated by Django 5.0.4 on 2024-05-03 12:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0022_cast_movie_cast'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='cast',
        ),
    ]
