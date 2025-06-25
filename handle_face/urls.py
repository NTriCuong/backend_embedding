from django.urls import path
from . import views

urlpatterns = [
  path('', views.run_camera, name='run_camera'),
]