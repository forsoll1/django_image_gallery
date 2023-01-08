from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ImageUpload.models import Album, Image
from account.models import Settings
from account.forms import SettingsForm

from django.core.exceptions import ValidationError, PermissionDenied
import random

def home(request):
    if request.user.is_authenticated:
        images = Image.objects.filter(user = request.user)
        if len(images)>4:
            random_images = random.sample(list(images), 4)
            images = random_images
            print(len(images))

        albums = Album.objects.filter(user = request.user)
        user_settings = Settings.objects.get(user = request.user)
        context =   {   'images': images,
                        'albums': albums, 
                        'show_slideshow':str(user_settings.show_slideshow)
                    }
        return render(request, 'home.html', context)
    return render(request, 'welcome.html')

@login_required
def user_settings(request):
    next = request.POST.get('next', '/')
    
    if request.method == 'POST':
        if 'return' in request.POST:
            return redirect(next)

        form = SettingsForm(request.POST)
        if form.is_valid:
            settings_instance = Settings.objects.get(user = request.user)
            if 'show_slideshow' in request.POST: settings_instance.show_slideshow = True
            else: settings_instance.show_slideshow = False

            settings_instance.save()
        else:
            raise(ValidationError, "Could not validate form")
        return redirect(next)
    else:
        context = { 'form': SettingsForm(instance = Settings.objects.get(user = request.user)),
                    'auth': request.user.is_authenticated}
    return render(request, 'settings.html', context)  

@login_required
def albumgallery(request, album_id):
    
    print(request)
    print(request.GET)

    chosen_album = Album.objects.get(id = album_id)
    images = Image.objects.filter(album = chosen_album)

    if 'old_to_new' in request.GET:
        print("GETOLD")
        images = images.order_by('-pub_date')

    if 'new_to_old' in request.GET:
        print("GETNEW")
        images = images.order_by('pub_date')

    if chosen_album.user == request.user:
        context = {
            'album': chosen_album,
            'images': images,
        }
        return render(request, 'gallery/albumgallery.html', context)
    else: 
        raise PermissionDenied()

@login_required
def view_image(request, image_id):
    chosen_image = Image.objects.get(id = image_id)

    if chosen_image.user == request.user:
        current_album = chosen_image.album
        get_user_albums = list(Album.objects.filter(user = request.user))
        user_albums = [a for a in get_user_albums if a.id != current_album.id]
        if len(user_albums) == 0:
            user_albums = None
        user_images = list(Image.objects.filter(album = current_album))
        chosen_index = user_images.index(chosen_image)

        next_image = None
        previous_image = None

        if len(user_images) == 1:
            pass
        elif chosen_index == len(user_images)-1:
            next_image = user_images[0]
            previous_image = user_images[chosen_index-1]
        elif chosen_index == 0:
            next_image = user_images[chosen_index+1]
            previous_image = user_images[len(user_images)-1]
        else:
            next_image = user_images[chosen_index+1]
            previous_image = user_images[chosen_index-1]
            
        context = { 'image': chosen_image,
                    'next': next_image,
                    'previous': previous_image,
                    'album': current_album,
                    'user_albums': user_albums}
        return render(request, 'gallery/image.html', context)
    else: 
        raise PermissionDenied()

@login_required
def delete(request, image_id):
    chosen_image = Image.objects.get(id = image_id)
    current_album = chosen_image.album

    if request.user == chosen_image.user:
        try:
            chosen_image.delete()
        except Exception as e: 
            print("Could not delete entry: " +str(e))
        return redirect('albumgallery', current_album.id) 
    else:
        raise PermissionDenied()

@login_required
def delete_album(request, album_id):

    chosen_album = Album.objects.get(id=album_id)
    if request.user == chosen_album.user:
        try:
            chosen_album.delete()
        except Exception as e: 
            print("Could not delete entry: " +str(e))
        return redirect('home') 
    else:
        raise PermissionDenied()

@login_required
def move_image(request):

    if request.method == 'POST':
        chosen_image = Image.objects.get(id = request.POST['image'])
        old_album = chosen_image.album
        new_album = Album.objects.get(id = request.POST['newalbum'])

        if chosen_image.user == request.user and new_album.user == request.user:
            chosen_image.album = new_album
            chosen_image.save()
            return redirect('albumgallery', old_album.id)
        else: 
            raise PermissionDenied()
    
    print('Could not move image between albums. Returning home.')
    return redirect('home') 

