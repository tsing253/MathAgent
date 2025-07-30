from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL
from dotenv import load_dotenv
import os
from django.db import transaction
from app.models import Group, Conversation, Dialogue, User
from django.utils import timezone
from rest_framework import serializers, status
from app.serializers import ConversationSerializer, ConversationCreateSerializer

load_dotenv(".env")

class test(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """测试接口"""
        return Response({"message": "Hello, this is a test endpoint!"}, status=status.HTTP_200_OK)

class SaveConversation(APIView):
    authentication_classes = []  # 允许匿名访问
    permission_classes = []

    def post(self, request):
        """保存对话内容，支持新对话创建和已有对话更新"""
        # 验证必需字段
        user_input = request.data.get('user_input')
        agent_output = request.data.get('agent_output')
        
        if not user_input or not agent_output:
            return Response(
                {"error": "Both user_input and agent_output are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation_id = request.data.get('conversation_id')
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        try:
            with transaction.atomic():
                # 处理对话（新对话或已有对话）
                if conversation_id:
                    # 继续现有对话
                    conversation = Conversation.objects.get(id=conversation_id)
                    created = False
                else:
                    # 创建新对话：使用用户输入的前20字符作为标题
                    title = request.data.get('title') or user_input[:20] + "..."
                    conversation = Conversation.objects.create(
                        user=user,
                        title=title
                    )
                    created = True
                
                # 保存对话内容
                Dialogue.objects.create(
                    conversation=conversation,
                    content=user_input,
                    reply=agent_output
                )
            
            return Response({
                "status": "success",
                "conversation_id": conversation.id,
                "title": conversation.title,
                "new_conversation": created
            }, status=status.HTTP_201_CREATED)
        
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CozeProxyAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        """Coze 代理接口（流式响应）"""
        # 参数验证
        message = request.data.get('message')
        conversation_id = request.data.get('conversation_id')
        
        if not message:
            return Response({"error": "Message content required"}, status=status.HTTP_400_BAD_REQUEST)

        # 初始化 Coze 客户端
        coze_api_token = os.getenv('COZE_API_TOKEN')
        bot_id = os.getenv("BOTID")
        
        if not all([coze_api_token, bot_id]):
            return Response({"error": "Service configuration error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            coze = Coze(
                auth=TokenAuth(token=coze_api_token),
                base_url=COZE_CN_BASE_URL
            )

            # 流式对话处理
            events = coze.chat.stream(
                bot_id=bot_id,
                user_id=str(request.user.id),  # 使用真实用户ID
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
                content_type='text/event-stream',
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
