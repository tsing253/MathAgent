from django.shortcuts import render, HttpResponse, redirect
from dotenv import load_dotenv
import requests
import json

load_dotenv(".env")

# Create your views here.
def login(request):
    if request.method == "GET":
        # 如果是 GET 请求，渲染登录页面
        return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        api_payload = {
            "username": username,
            "password": password
        }

        # 准备请求头，如果您的 API 需要认证 Token
        # token = f"Bearer {os.getenv('YOUR_AUTH_TOKEN', '')}"
        # headers = {
        #     "Authorization": token,
        #     "Content-Type": "application/json"
        # }
        # 如果不需要 Token，则为
        headers = {
            "Content-Type": "application/json"
        }

        error_message = None
        try:
            # 发送 POST 请求到后端登录 API
            response = requests.post("/api/login/", headers=headers, json=api_payload)

            # 检查 API 的响应状态码
            if response.status_code == 200:
                # API 成功，解析响应数据
                api_response_data = response.json()

                # 从 API 响应中提取用户信息
                user_id = api_response_data.get("user_id")
                user_username = api_response_data.get("username")
                user_name = api_response_data.get("name")
                user_role = api_response_data.get("role")

                if user_id and user_username and user_name and user_role:
                    # 将用户登录信息存储到 Django session 中
                    request.session['user_id'] = user_id
                    request.session['username'] = user_username
                    request.session['name'] = user_name
                    request.session['role'] = user_role

                    # 登录成功，重定向到 main 页面
                    return redirect("/main/")
                else:
                    # API 响应数据不完整
                    error_message = "从后端 API 接收到的用户信息不完整。"

            elif response.status_code == 401:
                # API 返回认证失败
                # 尝试从 API 响应中获取更具体的错误信息
                try:
                    error_detail = response.json().get("detail", "用户名或密码错误。")
                    error_message = error_detail
                except json.JSONDecodeError:
                    error_message = "用户名或密码错误。"
            else:
                # 其他 HTTP 错误
                error_message = f"登录失败，API 返回状态码: {response.status_code}"
                try:
                    # 尝试获取 API 返回的错误详情
                    error_detail = response.json().get("detail", "未知错误。")
                    error_message += f" - {error_detail}"
                except json.JSONDecodeError:
                    pass # 忽略无法解析 JSON 的错误

        except requests.exceptions.ConnectionError:
            error_message = "无法连接到后端登录服务，请检查网络连接和 API 地址。"
        except requests.exceptions.Timeout:
            error_message = "与后端登录服务的连接超时。"
        except requests.exceptions.RequestException as e:
            # 捕获其他 requests 库可能抛出的异常
            error_message = f"登录时发生错误: {e}"
        except ValueError:
            # 捕获 JSON 解析错误
            error_message = "解析后端 API 响应失败。"

        # 如果发生任何错误，返回登录页面并显示错误信息
        return render(request, "login.html", {"error": error_message})


def main(request):
    # 调用API创建会话并记录conversation_id
    # 加载环境变量
    # load_dotenv(".env")
    # token = f"Bearer {os.getenv('COZE_API_TOKEN', '')}"
    # botid = os.getenv("BOTID")
    # if not botid or not token:
    #     print(token, botid)
    #     return HttpResponse("BotID or token not found in environment variables.")
    # url = 'https://api.coze.cn/v1/conversation/create'
    # headers = {
    #     "Authorization": token,
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "bot_id": botid,
    #     "connector_id": "1024"
    # }
    
    error_message = None
    # try:
    #     response = requests.post(url, headers=headers, json=data)
    #     response.raise_for_status()  # 检查HTTP错误
    #     response_data = response.json()
    #     print(response_data)
    #     conversation_id = response_data.get('data', {}).get('id')
        
    #     if conversation_id:
    #         # 将conversation_id存入session
    #         request.session['conversation_id'] = conversation_id
            
    #         # 创建新的会话记录
    #         user_id = request.session.get('user_id')
    #         if user_id:
    #             Conversation.objects.create(
    #                 user_id=user_id,
    #                 title="新会话",
    #                 coze_conversation_id=conversation_id
    #             )
    #     else:
    #         error_message = "API响应中未找到conversation_id"
    # except requests.exceptions.HTTPError as e:
    #     error_message = f"API请求失败: {e}"
    # except requests.exceptions.RequestException as e:
    #     error_message = f"网络错误: {e}"
    # except ValueError as e:
    #     error_message = f"解析响应失败: {e}"
    
    # 将错误信息传递到模板
    context = {'error': error_message} if error_message else {}
    print("Conversation ID:", request.session.get('conversation_id', '未设置'))
    return render(request, "main.html", context)
