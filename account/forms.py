from django import forms
from .models import Settings

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('show_slideshow',)
        labels = {'show_slideshow': 'Enable slideshow on main gallery page'}