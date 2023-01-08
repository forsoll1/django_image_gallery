from django.contrib import admin

from .models import Settings

class SettingsAdmin(admin.ModelAdmin):
    fields = ['show_slideshow']
    list_display = ('user','show_slideshow',)

admin.site.register(Settings, SettingsAdmin)
