# Generated by Django 5.0.4 on 2024-04-28 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movies_tagline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='overview',
            field=models.CharField(max_length=1000),
        ),
    ]
