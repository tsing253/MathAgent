from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.backend_views import (
    UserViewSet, GroupViewSet, ConversationViewSet,
    DialogueViewSet, TestView, CozeProxyAPI
)

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'conversations', ConversationViewSet, basename='conversation')

# 嵌套路由：对话内容属于特定对话
conversation_router = DefaultRouter()
conversation_router.register(r'dialogues', DialogueViewSet, basename='conversation-dialogue')

urlpatterns = [
    # API文档
    path('', include(router.urls)),
    # 认证相关
    path('auth/', include('rest_framework.urls')),
    # 测试接口
    path('test/', TestView.as_view(), name='test'),
    # AI代理接口
    path('coze-proxy/', CozeProxyAPI.as_view(), name='coze_proxy'),
    # 嵌套对话内容路由
    path('conversations/<int:conversation_pk>/', include(conversation_router.urls)),
]