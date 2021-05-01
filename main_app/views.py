from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
from .models import Photo
from django.http import HttpResponse

# AWS
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'snapper-app'

# Create your views here.

# home view


def home(request):
    photos = Photo.objects.all()
    return render(request, 'home.html', {'photos': photos})


# photos view
def photos_detail(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    return render(request, 'photos/detail.html', {'photo': photo})


def photos_create(request):
    return render(request, 'photos/create.html')

# upload photo


def upload_photo(request):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            if request.POST['privacy'] == 'on':
                privacy = True
            else:
                privacy = False
            photo = Photo(
                url=url, title=request.POST['title'], privacy=privacy)
            photo.save()
        except:
            print('An error occurred creating photo')
    return redirect('home')


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['title', 'privacy']


class PhotoDelete(DeleteView):
    model = Photo
    success_url = '/'
