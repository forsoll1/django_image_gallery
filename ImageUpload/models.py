from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os, re
from random import randint

from PIL import Image as pil

def user_directory_path(instance, filename):
    randomizer = "_"+str(randint(1,999))
    file, ext = os.path.splitext(filename)
    filefolder = file+randomizer
    new_name = file+randomizer+ext
    return 'user_{0}/{1}/{2}'.format(instance.user.username, filefolder, new_name)

def add_resized_images(instance_id):

    img_instance = Image.objects.get(id = instance_id)
    img_path = img_instance.img_file.path
    im = pil.open(img_path)

# Change resolution of resized images here: 
    sizes = {  
        'small': 320,
        'medium': 640,
        'large': 1024,
        }

    resized_images = create_resized(im, img_path, sizes)

    # If some resized images were not made due to the original being too small, the ImageFields will get paths to existing images
    if 'small' not in resized_images:
        resized_images['small'] = re.split("/media/", img_path, 1)[-1]
    if 'medium' not in resized_images:
        resized_images['medium'] = resized_images['small']
    if 'large' not in resized_images:
        resized_images['large'] = resized_images['medium']

    img_instance.img_thumb = resized_images['thumb']
    img_instance.img_s = resized_images['small']
    img_instance.img_m = resized_images['medium']
    img_instance.img_l = resized_images['large']
    img_instance.save()

def create_resized(im, img_path, sizes):
    resized_images = {}
    width, height = im.size
    ratio = width/height

    for name, reso in sizes.items():

        #Forego creation of additional images if the original image is smaller than the resize target
        if reso <= width or reso <= height:
            file, ext = os.path.splitext(img_path)
            path = file + f"_{name}{ext}"

            new_width = reso
            new_height = new_width/ratio

            if width > height:
                new_width = reso
                new_height = new_width/ratio
            else: 
                new_height = reso
                new_width = new_height*ratio
            new_image = im.resize((round(new_width), round(new_height)), pil.ANTIALIAS)
            new_image.save(path, quality=95, optimize=True)
            resized_images[name] = re.split("/media/", path, 1)[-1]

    resized_images['thumb'] = create_thumbnail(im, img_path)
    return resized_images

def create_thumbnail(im, img_path):
    file, ext = os.path.splitext(img_path)
    thumb_path = file+"_thumb.jpeg"
    new_path = re.split("/media/", thumb_path, 1)[-1]

    # Convert the picture's mode and create a white background for the image, transparent pixels become white
    if im.mode in ("RGBA", "P"):
        new_image = pil.new("RGBA", im.size, "WHITE")
        new_image.paste(im, mask=im)

        im = new_image
        im = im.convert("RGB")
    
    size = (180,180)
    im.thumbnail(size)
    im.save(thumb_path, 'JPEG')
    
    return new_path

def delete_files_and_folder(chosen_image, user):
        file, ext = os.path.splitext(chosen_image.img_file.name)
        filename = re.split(r'\/', file)[-1]
        del_folder = f"{settings.BASE_DIR}{settings.MEDIA_URL}user_{user.username}/{filename}"
 
        for f in os.listdir(del_folder):
            os.remove(f"{del_folder}/{f}")   
        os.rmdir(del_folder)
        
        return    

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=50, help_text="Max 50 characters")

    def __str__(self):
        return self.album_name

    def delete(self, *args, **kwargs):
        images = Image.objects.filter(album = self)
        for i in images:
            i.delete()
        super(Album, self).delete(*args, **kwargs)

class Image(models.Model):  

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, help_text="Max 50 characters")
    img_file = models.ImageField(upload_to = user_directory_path, max_length=250)
    pub_date = models.DateTimeField(auto_now=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    # Resized image versions: 
    img_thumb = models.ImageField(upload_to = 'media/', blank=True, max_length=250)
    img_s = models.ImageField(upload_to = 'media/', blank=True, max_length=250)
    img_m = models.ImageField(upload_to = 'media/', blank=True, max_length=250)
    img_l = models.ImageField(upload_to = 'media/', blank=True, max_length=250)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Image, self).save(*args, **kwargs)
        if created: 
            add_resized_images(self.pk)

    def delete(self, *args, **kwargs):
        delete_files_and_folder(self, self.user)
        super(Image, self).delete(*args, **kwargs)


   




