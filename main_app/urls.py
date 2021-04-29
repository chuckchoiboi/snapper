from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # photos
    path('photos/<int:photo_id>/', views.photos_detail, name='detail'),
    # path('photos/create/', views.photos_create, name='photos_create'),
    # path('photos/<int:pk>/update/', views.photos_update, name='photos_update'),
    # path('photos/<int:pk>/delete/', views.photos_delete, name='photos_delete'),

    # account urls
    # path('accounts/signup/', views.signup, name='signup'),
]
