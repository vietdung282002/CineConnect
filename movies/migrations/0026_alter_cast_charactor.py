# Generated by Django 5.0.4 on 2024-05-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0025_cast_movie_cast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='charactor',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
