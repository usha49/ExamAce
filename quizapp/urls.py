# quizapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('test/', views.take_test, name='take_test'),
]
