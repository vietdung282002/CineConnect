# Generated by Django 5.0.4 on 2024-05-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0009_remove_customuser_favourite_delete_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.CharField(default='default.jpg'),
        ),
    ]
