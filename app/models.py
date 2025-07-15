from django.db import models

# makemigrations + migrate
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32, unique=True, default="")
    password = models.CharField(max_length=64, default="")
    name = models.CharField(max_length=32, default="")
    role = models.CharField(max_length=10, choices=[('student', '学生'), ('teacher', '老师')])

    def __str__(self):
        return self.username
    