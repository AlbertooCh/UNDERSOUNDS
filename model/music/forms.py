from django import forms
from model.music.music_models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        exclude = ['artist_name']  # Still exclude artist_name
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }
