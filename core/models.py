from django.db import models
import uuid
from django.conf import settings
from django.utils import timezone

class Movie(models.Model):

    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('sports', 'Sports'),
        ('reality_series', 'Reality Series'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
    ]

    uu_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to='movie_images/')
    image_cover = models.ImageField(upload_to='movie_images/')
    movie_views = models.IntegerField(default=0)
    youtube_video_id = models.CharField(max_length=20, blank=True, null=True)
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

class MovieList(models.Model):
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('owner_user', 'name')  # This enforces unique MovieList per user and name

    def __str__(self):
        return self.name


class CustomMovieList(models.Model):
    owner_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
