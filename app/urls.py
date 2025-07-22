# app/urls.py
from django.urls import path
from app import views

urlpatterns = [
    path("login/", views.login),
    path("", views.login),
    path("main/", views.main),
]