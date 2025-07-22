from django.db import models
from django.utils import timezone

# makemigrations + migrate
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32, unique=True, default="")
    password = models.CharField(max_length=64, default="")
    name = models.CharField(max_length=32, default="")
    role = models.CharField(max_length=10, choices=[('student', '学生'), ('teacher', '老师')])

    def __str__(self):
        return self.username

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=100, default="新会话")
    coze_conversation_id = models.CharField(max_length=100)  # 存储coze API返回的conversation_id
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.title}"

    class Meta:
        ordering = ['-updated_at']  # 按更新时间倒序排列