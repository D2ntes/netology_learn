from django import forms
from .models import Article

from ckeditor.widgets import CKEditorWidget


class Review(forms.ModelForm):
    description_art = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = ['title_art', 'description_art', 'published_at']
