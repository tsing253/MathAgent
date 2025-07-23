from django.db import models
from django.utils import timezone

# 用户模型
class User(models.Model):
    username = models.CharField(max_length=32, unique=True, default="")
    password = models.CharField(max_length=64, default="")
    name = models.CharField(max_length=32, default="")
    role = models.CharField(max_length=10, choices=[('student', '学生'), ('teacher', '老师')])

# 群组模型
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='group_memberships')
    created_at = models.DateTimeField(auto_now_add=True)
    

# 会话模型
class Conversation(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    

# 对话模型
class Dialogue(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='dialogues')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    reply = models.TextField(blank=True)
    
    