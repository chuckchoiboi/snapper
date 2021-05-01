from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid
import boto3
from .models import Photo, User
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
            if request.POST.get('privacy', None):
                privacy = True
            else:
                privacy = False

            userId = User.objects.get(username=request.user).pk
            photo = Photo(
                url=url,  title=request.POST['title'], privacy=privacy)
            photo.author_id = userId
            photo.save()
        except:
            print('An error occurred creating photo')
    return redirect('detail', photo_id=photo.pk)


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['title', 'privacy']


class PhotoDelete(DeleteView):
    model = Photo
    success_url = '/'


# Signup
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
