# Generated by Django 5.0.6 on 2024-07-12 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_movielist_movie_movielist_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='youtube_video_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]