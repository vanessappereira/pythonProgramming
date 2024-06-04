from django.urls import path
from . import views

# Define URL patterns for this Django application
urlpatterns = [
    path('', views.response, name='names'),
]