from django.core.management.base import BaseCommand
from app.models import User

class Command(BaseCommand):
    help = '创建示例用户数据'

    def handle(self, *args, **options):
        # 创建管理员用户
        User.objects.create(
            id=1,
            username='admin',
            password='admin',
            name='',
            role='管理员'
        )
        self.stdout.write(self.style.SUCCESS('成功创建管理员用户'))

        # 创建学生用户
        User.objects.create(
            id=5,
            username='student1',
            password='123456',
            name='张三',
            role='student'
        )
        self.stdout.write(self.style.SUCCESS('成功创建学生用户'))

        # 创建教师用户
        User.objects.create(
            id=6,
            username='teacher1',
            password='123456',
            name='李老师',
            role='teacher'
        )
        self.stdout.write(self.style.SUCCESS('成功创建教师用户'))

        self.stdout.write(self.style.SUCCESS('所有示例数据创建完成！'))