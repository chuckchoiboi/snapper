from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Photo
from django.http import HttpResponse

# Create your views here.

# home view


def home(request):
    photos = Photo.objects.all()
    return render(request, 'home.html', {'photos': photos})


# photos view
def photos_detail(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    return render(request, 'photos/detail.html', {'photo': photo})


class PhotoCreate(CreateView):
    model = Photo
    fields = ['url', 'title', 'privacy']
    success_url = '/'


class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['title', 'privacy']


class PhotoDelete(DeleteView):
    model = Photo
    success_url = '/'
