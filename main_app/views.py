from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import uuid
import boto3
from django.db.models import Q
from .models import Photo, User, Interaction
from django.http import HttpResponse

# AWS
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'snapper-app'

# Create your views here.


# home view

def home(request):
    if request.user.is_authenticated:
        photos = Photo.objects.filter(
            Q(privacy=False) | Q(author=request.user)).order_by('-created_at')
    else:
        photos = Photo.objects.filter(privacy=False).order_by('-created_at')
    return render(request, 'home.html', {'photos': photos})


# photos view
def photos_detail(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if photo.privacy == True:
        if photo.author == request.user:
            return render(request, 'photos/detail.html', {'photo': photo})
        else:
            print(request.user)
            return render(request, 'photos/detail.html', {'no_access': True})
    else:
        return render(request, 'photos/detail.html', {'photo': photo})


@login_required
def photos_create(request):
    return render(request, 'photos/create.html')

# user created photos


@login_required
def photos_user(request):
    photos = Photo.objects.filter(author=request.user)
    return render(request, 'photos/user.html', {'photos': photos})


# upload photo
@login_required
def upload_photo(request):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        print(photo_file)
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
            print(photo)
        except:
            print('An error occurred creating photo')
    return redirect('detail', photo_id=photo.pk)


class PhotoUpdate(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['title', 'privacy']


class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'


@login_required
def interact_photo(request, photo_id):
    userId = User.objects.get(username=request.user).pk
    photoId = Photo.objects.get(id=photo_id).pk
    interaction_type = request.GET.get('interaction')
    interaction = Interaction(
        interaction=interaction_type
    )
    interaction.user_id = userId
    interaction.photo_id = photoId
    print(interaction)
    interaction.save()
    return redirect('detail', photo_id=photoId)

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
