# Generated by Django 5.0.4 on 2024-05-09 16:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0035_rename_charactor_cast_character'),
        ('rating', '0002_rename_rating_rating_rate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ('rate',)},
        ),
        migrations.RemoveConstraint(
            model_name='rating',
            name='unique_movie_user_combination',
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('user', 'movie'), name='unique_movie_user_rating'),
        ),
    ]
