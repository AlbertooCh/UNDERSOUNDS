from django import forms
from model.Dto.music_dto import SongDTO
from django.core.validators import FileExtensionValidator


class SongForm(forms.Form):
    title = forms.CharField(
        label="Título",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    genre = forms.CharField(
        label="Género",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    price = forms.DecimalField(
        label="Precio",
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    release_date = forms.DateField(
        label="Fecha de lanzamiento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    album_cover = forms.ImageField(
        label="Portada del álbum",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    song_file = forms.FileField(
        label="Archivo de audio",
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])]
    )

    def clean_song_file(self):
        song_file = self.cleaned_data.get('song_file', False)

        # Si no se subió un nuevo archivo y la instancia ya tiene uno
        if not song_file and hasattr(self.instance, 'song_file') and self.instance.song_file:
            return self.instance.song_file

        # Si es una creación nueva y no se subió archivo
        if not song_file and not self.instance.pk:
            raise forms.ValidationError("Este campo es obligatorio.")

        # Si se subió un archivo vacío (por ejemplo, el usuario hizo clic en "clear")
        if song_file is None:
            raise forms.ValidationError("Este campo es obligatorio.")

        return song_file

class AlbumForm(forms.Form):
    title = forms.CharField(
        label="Título del álbum",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    genre = forms.CharField(
        label="Género",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    price = forms.DecimalField(
        label="Precio (€)",
        max_digits=8,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        }),
        required=True
    )

    release_date = forms.DateField(
        label="Fecha de lanzamiento",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=True
    )

    cover_image = forms.ImageField(
        label="Portada del álbum",
        widget=forms.FileInput(attrs={
            'class': 'form-control file-input',
            'accept': 'image/*'
        }),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=True
    )



