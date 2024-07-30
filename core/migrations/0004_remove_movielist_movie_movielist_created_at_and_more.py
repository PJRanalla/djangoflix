# Generated by Django 5.0.6 on 2024-07-08 22:54

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_movie_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movielist',
            name='movie',
        ),
        migrations.AddField(
            model_name='movielist',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='movielist',
            name='movies',
            field=models.ManyToManyField(to='core.movie'),
        ),
        migrations.AddField(
            model_name='movielist',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='uu_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
