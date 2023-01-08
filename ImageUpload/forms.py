from django import forms
from .models import Image, Album

class ImageForm(forms.ModelForm):

    album_choice = forms.ModelChoiceField(queryset=Album.objects.all(), label='Album', empty_label=None)

    class Meta:
        model = Image
        fields = ('img_file', 'description')
        labels = {'img_file': 'Your image ', 'description': 'Description '}

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_name']
