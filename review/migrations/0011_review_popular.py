# Generated by Django 5.0.4 on 2024-06-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_alter_review_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='popular',
            field=models.FloatField(default=0),
        ),
    ]