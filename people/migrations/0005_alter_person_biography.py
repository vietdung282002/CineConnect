# Generated by Django 5.0.4 on 2024-05-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('people', '0004_alter_person_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='biography',
            field=models.TextField(blank=True, null=True),
        ),
    ]
