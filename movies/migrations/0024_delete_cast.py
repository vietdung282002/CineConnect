# Generated by Django 5.0.4 on 2024-05-03 12:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0023_remove_movie_cast'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cast',
        ),
    ]
