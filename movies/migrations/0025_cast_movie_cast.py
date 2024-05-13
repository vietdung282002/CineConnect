# Generated by Django 5.0.4 on 2024-05-03 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('movies', '0024_delete_cast'),
        ('people', '0012_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('charactor', models.CharField(blank=True, max_length=200)),
                ('order', models.IntegerField(null=True)),
                ('cast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.person')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='casts',
                                            to='movies.movie')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(related_name='movies', through='movies.Cast', to='people.person'),
        ),
    ]
