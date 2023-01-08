# Django based image gallery

### Launching the app
Excute at root: <br>
<code>[your python compiler] manage.py runserver</code> <br>
This will start the app at 127.0.0.1:8000
Admin credentials: 
Username admin
Password password

### Description

This web application allows a registered user to upload, organize and view images. The images are linked to user-created folders for simple organization 
and can be moved between folders or deleted. Folder contents are displayed as thumbnail-galleries.  
As the user uploads an image, depending on the size of the image it gets resized up to three different size categories and stored to a physical location.
As images are viewed the app can then offer a suitable image size depending on the user's viewport size. 

Visual look is done with Bootstrap and authentication is handled with Django's auth functionality. 
