# Generated by Django 5.0.4 on 2024-04-28 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_alter_movie_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
