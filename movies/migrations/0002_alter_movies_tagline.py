# Generated by Django 5.0.4 on 2024-04-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='tagline',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
