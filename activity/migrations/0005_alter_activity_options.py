# Generated by Django 5.0.4 on 2024-06-16 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_activity_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ('-time_stamp',)},
        ),
    ]