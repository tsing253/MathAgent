from django.http import JsonResponse 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from api.models import User 

class DynamicFieldsSerializer(serializers.Serializer):
    """
    动态字段序列化器，根据视图需要动态创建字段
    """
    @classmethod
    def create_for_view(cls, fields):
        return type('DynamicSerializer', (serializers.Serializer,), fields)

class BaseAPIView(APIView):
    """
    基础 API 视图，支持动态序列化器
    """
    serializer_fields = {}
    
    def get_serializer_class(self):
        return DynamicFieldsSerializer.create_for_view(self.serializer_fields)
    
    def get_serializer(self, data=None):
        serializer_class = self.get_serializer_class()
        return serializer_class(data=data)
    
# 登录视图
class LoginView(BaseAPIView):
    serializer_fields = {
        'username': serializers.CharField(required=True),
        'password': serializers.CharField(required=True, write_only=True)
    }
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=400)
        
        # 从 request.POST 获取表单数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username or not password:
            return JsonResponse({"error": "用户名和密码是必需的"}, status=400)
        
        try:
            # 尝试从数据库中获取用户
            user = User.objects.get(username=username)
            
            # 检查密码是否匹配（实际应用中应使用密码哈希验证）
            if user.password == password:  # 注意：实际中应使用 check_password
                # 登录成功 - 设置 session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['name'] = user.name  # 假设用户模型有 name 字段
                request.session['role'] = user.role  # 假设用户模型有 role 字段
                
                return JsonResponse({
                    "message": "登录成功",
                    "user_id": user.id,
                    "username": user.username,
                    "name": user.name,
                    "role": user.role
                }, status=200)
            else:
                return JsonResponse({"error": "用户名或密码不正确"}, status=401)
                
        except User.DoesNotExist:
            return JsonResponse({"error": "用户不存在"}, status=404)
            
        except Exception as e:
            print(f"登录过程中发生错误: {e}")
            return JsonResponse({"error": "服务器内部错误"}, status=500)

# 聊天视图
class ChatView(BaseAPIView):
    serializer_fields = {
        'message': serializers.CharField(required=True),
        'conversation_id': serializers.CharField(required=False, allow_null=True)
    }
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=400)
        
        # 处理聊天逻辑...
        message = request.POST.get("message")
        
        # 这里可以添加处理聊天消息的逻辑
        response_message = f"Echo: {message}"
        return JsonResponse({"response": response_message}, status=200)
