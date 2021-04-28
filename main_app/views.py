from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# home view


def home(request):
    return render(request, 'home.html', {'photos': photos})


class Photo:
    def __init__(self, author, url, title, privacy, interactions):
        self.author = author
        self.url = url
        self.title = title
        self.privacy = privacy
        self.interactions = interactions


photos = [
    Photo('chuckchoiboi', 'https://user-images.githubusercontent.com/60675322/116333406-3adec180-a788-11eb-98ab-afdfbf6701b0.JPG',
          'Image 1', False, ['chuckchoiboi']),
    Photo('chuckchoiboi', 'https://user-images.githubusercontent.com/60675322/116333411-3ca88500-a788-11eb-8cb2-e4a7068ade84.JPG',
          'Image 2', False, ['chuckchoiboi']),
    Photo('chuckchoiboi', 'https://user-images.githubusercontent.com/60675322/116333416-3e724880-a788-11eb-8f60-f1f8b53a9d31.JPG',
          'Image 3', False, ['chuckchoiboi']),
]
