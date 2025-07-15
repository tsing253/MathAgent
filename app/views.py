from django.shortcuts import render, HttpResponse, redirect
from app.models import User

# Create your views here.

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
                request.session['role'] = user.role
                return redirect("/main/")
            else:
                error_message = "密码错误"
                return render(request, "login.html", {"error": error_message})
        except User.DoesNotExist:
            error_message = "用户不存在"
            return render(request, "login.html", {"error": error_message})


def main(request):
    return render(request, "main.html")

from app import models

def orm(request):
    models.User.objects.create(username='admin', password='admin')
    return HttpResponse("ORM operation completed, user created with username 'admin' and password 'admin'.")