from django.shortcuts import render, HttpResponse, redirect
from app.models import User
from dotenv import load_dotenv
import requests
import os

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

def orm(request):
    User.objects.create(username='admin', password='admin')
    return HttpResponse("ORM operation completed, user created with username 'admin' and password 'admin'.")