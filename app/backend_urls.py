from django.contrib import admin
from django.urls import path
from app import backend_views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('save-conversation/', backend_views.save_conversation, name='save_conversation'),
    path('coze-proxy/', backend_views.coze_proxy, name='coze_proxy'),
]