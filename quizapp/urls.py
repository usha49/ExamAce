# quizapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.take_test, name='take_test'),
]
