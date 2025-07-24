from django.contrib import admin
from django.urls import path
from app import frontend_views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", frontend_views.main),
    
    path("login/", frontend_views.login),
    path("main/", frontend_views.main),
]