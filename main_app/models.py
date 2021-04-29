from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=150)
    privacy = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("photo_detail", kwargs={"photo_id": self.pk})
