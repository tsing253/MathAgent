from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"Received username: {username}, password: {password}")  # 调试输出
        
        # 模拟登录验证
        return redirect("/main/")  # 登录成功后重定向到主页面


def main(request):
    return render(request, "main.html")