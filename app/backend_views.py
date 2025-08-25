from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL

from app.models import User, Group, Conversation, Dialogue
from app.serializers import (
    UserSerializer, GroupSerializer, ConversationSerializer,
    ConversationCreateSerializer, DialogueSerializer, DialogueCreateSerializer
)

import os

load_dotenv(".env")

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户管理 API
    
    list:
    获取所有用户列表
    * 需要认证
    * 返回用户基本信息
    
    retrieve:
    获取特定用户详情
    * 需要认证
    * 返回用户完整信息
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    群组管理 API
    
    list:
    获取所有群组列表
    * 需要认证
    * 返回群组及其成员信息
    
    create:
    创建新群组
    * 需要认证
    * 可以指定群组名称、描述和初始成员
    
    retrieve:
    获取特定群组详情
    * 需要认证
    * 返回群组完整信息，包括成员列表
    
    update:
    更新群组信息
    * 需要认证
    * 可以修改群组名称、描述等
    
    delete:
    删除群组
    * 需要认证
    * 将同时删除相关的会话记录
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """添加群组成员"""
        group = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "需要提供用户ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            group.members.add(user)
            return Response({"status": "success"})
        except User.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """移除群组成员"""
        group = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "需要提供用户ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            group.members.remove(user)
            return Response({"status": "success"})
        except User.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    对话管理视图集
    提供对话的CRUD操作
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取用户相关的对话列表"""
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """创建对话时自动关联当前用户"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def dialogues(self, request, pk=None):
        """获取特定对话的所有对话内容"""
        conversation = self.get_object()
        dialogues = conversation.dialogues.all().order_by('timestamp')
        serializer = DialogueSerializer(dialogues, many=True)
        return Response(serializer.data)

class DialogueViewSet(viewsets.ModelViewSet):
    """
    对话内容管理视图集
    提供对话内容的CRUD操作
    """
    serializer_class = DialogueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取特定对话的内容"""
        conversation_id = self.kwargs.get('conversation_pk')
        return Dialogue.objects.filter(
            conversation_id=conversation_id,
            conversation__user=self.request.user
        )

    def perform_create(self, serializer):
        """创建对话内容时关联到对话"""
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        serializer.save(conversation=conversation)

class TestView(APIView):
    """测试接口"""
    permission_classes = []

    def get(self, request):
        return Response({
            "message": "Hello, this is a test endpoint!",
            "api_version": "1.0"
        }, status=status.HTTP_200_OK)

class CozeProxyAPI(APIView):
    """Coze AI代理接口"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """处理AI对话请求（流式响应）"""
        message = request.data.get('message')
        conversation_id = request.data.get('conversation_id')
        
        if not message:
            return Response({
                "error": "Message content required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # 初始化Coze客户端
        coze_api_token = os.getenv('COZE_API_TOKEN')
        bot_id = os.getenv("BOTID")
        
        if not all([coze_api_token, bot_id]):
            return Response({
                "error": "Service configuration error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            coze = Coze(
                auth=TokenAuth(token=coze_api_token),
                base_url=COZE_CN_BASE_URL
            )

            # 处理流式对话
            events = coze.chat.stream(
                bot_id=bot_id,
                user_id=str(request.user.id),
                conversation_id=conversation_id,
                additional_messages=[Message.build_user_question_text(message)],
                auto_save_history=False
            )

            def event_stream():
                for event in events:
                    if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                        yield event.message.content

            return StreamingHttpResponse(
                event_stream(),
                content_type='text/event-stream'
            )

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
