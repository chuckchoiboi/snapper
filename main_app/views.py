from django.shortcuts import render
from .models import Photo
from django.http import HttpResponse

# Create your views here.

# home view


def home(request):
    return render(request, 'home.html', {'photos': photos})

# photos view


def photos_detail(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    return render(request, 'photos/detail.html', {'photo': photo})
