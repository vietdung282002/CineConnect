# Generated by Django 5.0.4 on 2024-05-01 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('adult', models.BooleanField(default=False)),
                ('biography', models.CharField(blank=True, max_length=1000, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('deathday', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')],
                                            default='others', max_length=20)),
                ('homepage', models.CharField(blank=True, max_length=200, null=True)),
                ('known_for_department', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('place_of_birth', models.CharField(max_length=200)),
                ('profile_path', models.ImageField(default='default.jpg', upload_to='pictures')),
            ],
        ),
    ]
