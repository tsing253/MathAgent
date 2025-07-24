from django.shortcuts import render, HttpResponse, redirect
from app.models import User
from dotenv import load_dotenv
import requests
import os
import json
from django.http import JsonResponse, StreamingHttpResponse

# Create your views here.

load_dotenv(".env")


# 添加会话保存视图
def save_conversation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST)
            # 这里实际应该将对话内容保存到数据库
            # 示例中只打印到控制台
            print(f"保存对话内容: {data}")
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=405)

# 添加Coze API代理视图
def coze_proxy(request):
    if request.method == 'POST':
        try:       
            # 从session获取conversation_id
            conversation_id = request.session.get('conversation_id', '')
            if not conversation_id:
                return JsonResponse({"error": "会话ID未找到"}, status=400)
            
            # 准备API参数
            token = f"Bearer {os.getenv('COZE_API_TOKEN', '')}"
            bot_id = os.getenv("BOTID")
            user_message = request.POST.get('message')
            
            # 构造API请求
            url = f'https://api.coze.cn/v3/chat?conversation_id={conversation_id}'
            headers = {
                "Authorization": token,
                "Content-Type": "application/json"
            }
            payload = {
                "bot_id": bot_id,
                "user_id": "123",
                "stream": True,
                "additional_messages": [
                    {
                        "role": "user",
                        "type": "question",
                        "content_type": "text",
                        "content": user_message
                    }
                ],
                "auto_save_history": False
            }
            
            # 调用Coze API
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                stream=True
            )
            
            # 流式响应处理
            def generate():
                for chunk in response.iter_lines():
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        if decoded_chunk.startswith('data:'):
                            try:
                                data = json.loads(decoded_chunk[5:])
                                content = data.get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                pass
            
            # 返回流式响应
            return StreamingHttpResponse(
                generate(), 
                content_type='text/event-stream'
            )
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "无效请求"}, status=400)