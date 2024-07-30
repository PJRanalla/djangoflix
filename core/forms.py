from django import forms
from .models import CustomMovieList

class CustomMovieListForm(forms.ModelForm):
    class Meta:
        model = CustomMovieList
        fields = ['name']
