from django.core.management.base import BaseCommand
from rest_framework.schemas.generators import EndpointEnumerator
from rest_framework import serializers

class Command(BaseCommand):
    help = '列出所有可用的 API 接口及其详细信息'

    def handle(self, *args, **options):
        enumerator = EndpointEnumerator()
        endpoints = enumerator.get_api_endpoints()
        
        self.stdout.write(self.style.SUCCESS('=== 可用的 API 接口列表 ===\n'))
        
        # 按路径前缀分组
        grouped_endpoints = {}
        for path, method, callback in endpoints:
            prefix = path.split('/')[1] if len(path.split('/')) > 1 else '根路径'
            if prefix not in grouped_endpoints:
                grouped_endpoints[prefix] = []
            grouped_endpoints[prefix].append((path, method, callback))
        
        # 打印分组后的接口
        for prefix, endpoints in grouped_endpoints.items():
            self.stdout.write(self.style.SUCCESS(f'\n[{prefix}] 相关接口:'))
            for path, method, callback in endpoints:
                # 获取视图类的文档字符串
                view_class = callback.cls if hasattr(callback, 'cls') else callback.__class__
                doc = view_class.__doc__ or '无描述'
                
                # 获取序列化器信息
                serializer_class = getattr(view_class, 'serializer_class', None)
                if serializer_class and issubclass(serializer_class, serializers.Serializer):
                    fields = serializer_class().fields.keys()
                    fields_info = f"字段: {', '.join(fields)}"
                else:
                    fields_info = "无序列化器信息"
                
                # 打印接口信息
                self.stdout.write(f"\n  {method} {path}")
                self.stdout.write(f"  描述: {doc.strip()}")
                self.stdout.write(f"  {fields_info}")
