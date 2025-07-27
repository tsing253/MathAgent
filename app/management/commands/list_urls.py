from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = '列出项目中的所有 URL 模式'

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        self.stdout.write('项目中的 URL 模式列表：')
        for pattern in url_patterns:
            self.stdout.write(str(pattern))