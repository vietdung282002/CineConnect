# Generated by Django 5.0.4 on 2024-05-03 11:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0019_cast_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='cast',
        ),
    ]
