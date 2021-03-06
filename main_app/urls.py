from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # photos
    path('photos/<int:photo_id>/', views.photos_detail, name='detail'),
    path('photos/create/', views.photos_create, name='photos_create'),
    path('photos/<int:pk>/update/',
         views.PhotoUpdate.as_view(), name='photos_update'),
    path('photos/<int:pk>/delete/',
         views.PhotoDelete.as_view(), name='photos_delete'),
    path('photos/myphotos/',
         views.photos_user, name='photos_user'),

    # route for photo upload
    path('photos/upload_photo', views.upload_photo, name='upload_photo'),

    # route for photo interaction
    path('photos/interact_photo/<int:photo_id>/',
         views.interact_photo, name='interact_photo'),

    # account urls
    path('accounts/signup/', views.signup, name='signup'),
]
