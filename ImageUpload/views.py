from django.shortcuts import render, redirect

from ImageUpload.forms import AlbumForm, ImageForm
from .models import Album

from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def upload(request):
    current_user = request.user

    if request.method == 'POST' and 'submit_album' in request.POST:
        albumform = AlbumForm(request.POST)
        if albumform.is_valid():
            try:
                instance = albumform.save(commit=False)
                instance.user = current_user
                instance.save()
                return redirect('upload')
            except Exception as e:
                print("Could not create Image entry: "+str(e))
                return redirect('home')
        else: 
            raise ValidationError
    
    if request.method == 'POST' and 'submit_image' in request.POST:
        imageform = ImageForm(request.POST, request.FILES)
        if imageform.is_valid():
            try:
                instance = imageform.save(commit=False)
                instance.user = current_user
                instance.album = imageform.cleaned_data['album_choice']
                instance.save()
                return redirect('home')
            except Exception as e:
                print("Problem with image creation: "+str(e))
                return redirect('home')
        else: 
            raise ValidationError

    user_albums = Album.objects.filter(user = request.user)

    imageform = ImageForm()
    albumform = AlbumForm()

    imageform.fields['album_choice'].queryset = user_albums

    context = { 'imageform': imageform, 
                'albumform': albumform,
                'albums': user_albums}

    return render(request, 'upload/upload.html', context)


    

    
