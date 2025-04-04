from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User

class FanRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'
        if commit:
            user.save()
        return user


class ArtistRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    artist_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    artist_type = forms.ChoiceField(
        choices=[('solo', 'Solo'), ('band', 'Band')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    genre = forms.ChoiceField(
        choices=[
            ('pop', 'Pop'),
            ('rock', 'Rock'),
            ('hiphop', 'Hip Hop/Rap'),
            ('electronic', 'Electrónica'),
            ('jazz', 'Jazz'),
            ('classical', 'Clásica'),
            ('reggaeton', 'Reggaetón'),
            ('indie', 'Indie'),
            ('other', 'Otro'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'artist_name', 'artist_type', 'bio', 'genre', 'country']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'artist'
        user.artist_name = self.cleaned_data['artist_name']
        user.artist_type = self.cleaned_data['artist_type']
        user.bio = self.cleaned_data['bio']
        user.genre = self.cleaned_data['genre']
        user.country = self.cleaned_data['country']
        if commit:
            user.save()
        return user
