from django.core.management.base import BaseCommand
from app.models import User, Group, Conversation, Dialogue
from django.utils import timezone

class Command(BaseCommand):
    help = '创建示例用户数据及相关测试数据'

    def handle(self, *args, **options):
        # 创建管理员用户
        admin = User.objects.create(
            id=1,
            username='admin',
            password='admin',
            name='管理员',
            role='admin'
        )
        self.stdout.write(self.style.SUCCESS('成功创建管理员用户'))

        # 创建学生用户
        student = User.objects.create(
            id=2,
            username='student1',
            password='123456',
            name='张三',
            role='student'
        )
        self.stdout.write(self.style.SUCCESS('成功创建学生用户'))

        # 创建教师用户
        teacher = User.objects.create(
            id=3,
            username='teacher1',
            password='123456',
            name='李老师',
            role='teacher'
        )
        self.stdout.write(self.style.SUCCESS('成功创建教师用户'))
        
        # 创建测试用户
        test_user = User.objects.create(
            id=4,
            username='test',
            password='testpass',
            name='测试用户',
            role='student'
        )
        self.stdout.write(self.style.SUCCESS('成功创建测试用户'))
        
        # ================= 创建测试群组 =================
        # 创建学习小组
        study_group = Group.objects.create(
            name="Python学习小组",
            description="Django和Python学习交流群"
        )
        study_group.members.add(test_user, student, teacher)
        self.stdout.write(self.style.SUCCESS('成功创建学习群组'))
        
        # 创建项目小组
        project_group = Group.objects.create(
            name="毕业设计项目组",
            description="2023届毕业设计协作群"
        )
        project_group.members.add(test_user, student)
        self.stdout.write(self.style.SUCCESS('成功创建项目群组'))
        
        # ================= 创建测试会话 =================
        # 学习小组的会话
        convo1 = Conversation.objects.create(
            title="Django模型讨论",
            group=study_group
        )
        
        convo2 = Conversation.objects.create(
            title="作业问题解答",
            group=study_group
        )
        
        # 项目小组的会话
        convo3 = Conversation.objects.create(
            title="项目需求分析",
            group=project_group
        )
        self.stdout.write(self.style.SUCCESS('成功创建3个会话'))
        