from django.core.management.base import BaseCommand
from django.core.cache import cache
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '显示网站访问统计'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清除访问统计缓存'
        )

    def handle(self, *args, **options):
        if options['clear']:
            cache.delete('visit_stats')
            self.stdout.write("已清除访问统计缓存")
            return
        try:
            stats = cache.get('visit_stats')
            if stats:
                # 统计IP访问次数
                ip_counter = defaultdict(int)
                # 修正循环逻辑，直接使用字典的值
                for ip, count in stats['ips'].items():
                    ip_counter[ip] = count
                
                total_visits = sum(ip_counter.values())
                unique_ips = len(ip_counter)
                
                self.stdout.write(f"总访问次数: {total_visits}")
                self.stdout.write(f"独立IP数量: {unique_ips}")
                self.stdout.write("IP访问详情:")
                for ip, count in sorted(ip_counter.items(), key=lambda x: x[1], reverse=True):
                    self.stdout.write(f"- {ip.ljust(15)} : {count} 次")
            else:
                logger.error("无法获取访问统计信息，缓存可能未正确配置")
                self.stdout.write("""
                    暂无访问统计信息，可能原因：
                    1. 中间件未运行
                    2. 缓存未正确配置
                    3. 尚未有访问记录""")
        except Exception as e:
            logger.error(f"获取统计信息时出错: {str(e)}")
            self.stdout.write(f"错误: {str(e)}")