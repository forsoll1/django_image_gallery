"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from account.views import SignUpView

from GalleryApp import views as gallery
from ImageUpload import views as imageupload
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('admin/', admin.site.urls),

    path('', gallery.home, name="home"),
    path('upload/', imageupload.upload, name="upload"),
    path('album/<int:album_id>', gallery.albumgallery, name='albumgallery'),
    path('album/<int:album_id>/delete', gallery.delete_album, name='delete_album'),
    path('image/<int:image_id>', gallery.view_image, name="view_image"),
    path('image/<int:image_id>/delete', gallery.delete, name="delete"),
    path('image/move', gallery.move_image, name="move_image"),
    
    path('settings/', gallery.user_settings, name="settings"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)