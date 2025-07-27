from django.urls import path
from app.backend_views import SaveConversation, CozeProxyAPI, test

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('save-conversation/', SaveConversation.as_view(), name='save_conversation'),
    path('coze-proxy/', CozeProxyAPI.as_view(), name='coze_proxy'),
    path('test/', test.as_view(), name='test_endpoint'),
]