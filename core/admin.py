from django.contrib import admin
from .models import Movie, MovieList, CustomMovieList

# Register your models here.
admin.site.register(Movie)
admin.site.register(MovieList)
admin.site.register(CustomMovieList)
