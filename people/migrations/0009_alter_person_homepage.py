# Generated by Django 5.0.4 on 2024-05-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('people', '0008_alter_person_known_for_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='homepage',
            field=models.TextField(blank=True, null=True),
        ),
    ]
