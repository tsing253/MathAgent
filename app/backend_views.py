from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL
from dotenv import load_dotenv
import requests
import os
import json
from django.http import JsonResponse, StreamingHttpResponse
from django.db import transaction
from app.models import Group, Conversation, Dialogue, User
from django.utils import timezone
# Create your views here.

load_dotenv(".env")


def save_conversation(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        
        # 校验必要字段
        required_fields = ['user_id', 'content']
        if not all(field in data for field in required_fields):
            return JsonResponse({"status": "error", "message": "缺少必要字段（user_id/content）"}, status=400)

        with transaction.atomic():
            # 获取或创建会话（优先使用现有会话）
            conversation_id = data.get('conversation_id')
            if conversation_id:
                # 验证会话所有权
                conversation = Conversation.objects.get(
                    id=conversation_id,
                    user_id=data['user_id']
                )
                created = False
            else:
                # 创建新会话
                conversation = Conversation.objects.create(
                    user_id=data['user_id'],
                    title=data.get('title', f"新会话 {timezone.now().strftime('%m-%d %H:%M')}")
                )
                created = True

            # 创建对话记录
            Dialogue.objects.create(
                conversation=conversation,
                content=data['content'],
                reply=data.get('reply', '')
            )

        return JsonResponse({
            "status": "success",
            "conversation_id": conversation.id,
            "new_conversation": created
        })

    except User.DoesNotExist:
        return JsonResponse({"status": "error", "message": "用户不存在"}, status=404)
    except Conversation.DoesNotExist:
        return JsonResponse({"status": "error", "message": "会话不存在或无权访问"}, status=403)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def coze_proxy(request):
    if request.method == 'POST':
        try:
            # 获取用户输入
            user_message = request.POST.get('message')
            if not user_message:
                return JsonResponse({"error": "消息内容不能为空"}, status=400)
            
            # 初始化Coze客户端
            coze_api_token = os.getenv('COZE_API_TOKEN')
            if not coze_api_token:
                return JsonResponse({"error": "未配置COZE_API_TOKEN"}, status=500)
            
            coze = Coze(
                auth=TokenAuth(token=coze_api_token),
                base_url=COZE_CN_BASE_URL
            )
            
            # 获取会话ID（支持多轮对话）
            conversation_id = request.session.get('conversation_id')
            bot_id = os.getenv("BOTID")
            if not bot_id:
                return JsonResponse({"error": "未配置BOTID"}, status=500)
            
            # 构建消息体
            additional_messages = [Message.build_user_question_text(user_message)]
            
            # 调用流式API
            events = coze.chat.stream(
                bot_id=bot_id,
                user_id="user123",  # 建议替换为真实用户ID
                conversation_id=conversation_id,
                additional_messages=additional_messages,
                auto_save_history=False
            )
            
            # 流式响应生成器
            def generate():
                new_conv_id = None
                for event in events:
                    if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                        yield event.message.content
                    elif event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                        new_conv_id = event.chat.conversation_id
                
                # 保存最新会话ID
                if new_conv_id:
                    request.session['conversation_id'] = new_conv_id
                    request.session.save()
            
            return StreamingHttpResponse(
                generate(),
                content_type='text/event-stream'
            )
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "仅支持POST请求"}, status=400)