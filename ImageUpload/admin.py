from django.contrib import admin

from ImageUpload.models import Image, Album

class ImageAdmin(admin.ModelAdmin):
    fields = ['user', 'img_file', 'description', 'album']
    list_display = ('id','album', 'pub_date', 'description')
    list_filter = ['pub_date']
    search_fields = ['description']

admin.site.register(Album)
admin.site.register(Image, ImageAdmin)