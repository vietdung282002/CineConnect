# Generated by Django 5.0.4 on 2024-05-09 13:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0034_alter_cast_options_alter_movie_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cast',
            old_name='charactor',
            new_name='character',
        ),
    ]
