from django.urls import path
from . import views

urlpatterns = [
  
    path("", views.home, name="home"),          # today
    path("archive/", views.archive, name="archive")
]
