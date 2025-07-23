from django.shortcuts import render, HttpResponse, redirect
from app.models import User
from dotenv import load_dotenv
import requests
import os
import json
from django.http import JsonResponse, StreamingHttpResponse

# Create your views here.

load_dotenv(".env")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
            if user.password == password:  # 注意：实际项目中应该使用加密密码
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['name'] = user.name
                request.session['role'] = user.role
                return redirect("/main/")
            else:
                error_message = "密码错误"
                return render(request, "login.html", {"error": error_message})
        except User.DoesNotExist:
            error_message = "用户不存在"
            return render(request, "login.html", {"error": error_message})


def main(request):
    # 调用API创建会话并记录conversation_id
    # 加载环境变量

    token = f"Bearer {os.getenv('COZE_API_TOKEN', '')}"
    botid = os.getenv("BOTID")
    if not botid or not token:
        print(token, botid)
        return HttpResponse("BotID or token not found in environment variables.")
    url = 'https://api.coze.cn/v1/conversation/create'
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "bot_id": botid,
        "connector_id": "1024"
    }
    
    error_message = None
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查HTTP错误
        response_data = response.json()
        print(response_data)
        conversation_id = response_data.get('data', {}).get('id')
        
        if conversation_id:
            # 将conversation_id存入session
            request.session['conversation_id']= conversation_id
        else:
            error_message = "API响应中未找到conversation_id"
    except requests.exceptions.HTTPError as e:
        error_message = f"API请求失败: {e}"
    except requests.exceptions.RequestException as e:
        error_message = f"网络错误: {e}"
    except ValueError as e:
        error_message = f"解析响应失败: {e}"
    
    # 将错误信息传递到模板
    context = {'error': error_message} if error_message else {}
    print("Conversation ID:", request.session.get('conversation_id', '未设置'))
    return render(request, "main.html", context)

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