from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('save_grade/', views.save_grade, name='save_grade'),
]