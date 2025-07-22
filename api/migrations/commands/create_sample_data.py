from django.core.management.base import BaseCommand
from app.models import User

class Command(BaseCommand):
    help = '创建示例用户数据'

    def handle(self, *args, **options):
        # 创建或更新管理员用户
        User.objects.update_or_create(
            id=1,
            defaults={
                'username': 'admin',
                'password': 'admin',
                'name': '',
                'role': '管理员'
            }
        )
        self.stdout.write(self.style.SUCCESS('成功创建/更新管理员用户'))

        # 创建或更新学生用户
        User.objects.update_or_create(
            id=5,
            defaults={
                'username': 'student1',
                'password': '123456',
                'name': '张三',
                'role': 'student'
            }
        )
        self.stdout.write(self.style.SUCCESS('成功创建/更新学生用户'))

        # 创建或更新教师用户
        User.objects.update_or_create(
            id=6,
            defaults={
                'username': 'teacher1',
                'password': '123456',
                'name': '李老师',
                'role': 'teacher'
            }
        )
        self.stdout.write(self.style.SUCCESS('成功创建/更新教师用户'))

        self.stdout.write(self.style.SUCCESS('所有示例数据创建/更新完成！'))