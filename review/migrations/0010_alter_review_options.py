# Generated by Django 5.0.4 on 2024-06-07 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_remove_reaction_dislike'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-time_stamp',)},
        ),
    ]
