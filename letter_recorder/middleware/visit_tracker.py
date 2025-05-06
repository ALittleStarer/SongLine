import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class VisitTrackerMiddleware:
    def __init__(self, get_response):
        logger.info("VisitTrackerMiddleware initialized")  # 添加初始化日志
        self.get_response = get_response

    def __call__(self, request):
        logger.info("VisitTrackerMiddleware processing request")  # 添加请求处理日志
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        logger.info(f"Recording visit from IP: {ip}")
        
        # 更新访问统计
        cache_key = 'visit_stats'
        stats = cache.get(cache_key, {'count': 0, 'ips': {}})
        
        # 数据迁移逻辑：如果ips是旧版list格式，转换为新版dict格式
        if isinstance(stats['ips'], list):
            stats['ips'] = {ip:1 for ip in stats['ips']}
            logger.warning("Detected legacy IP list format, migrating to dict format")
            
        # 确保数据结构正确
        stats['ips'] = stats.get('ips', {})
        stats['count'] = stats.get('count', 0)
        
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        # 删除错误的count累加
        stats['ips'][client_ip] = stats['ips'].get(client_ip, 0) + 1
        stats['count'] = sum(stats['ips'].values())  # 正确的总访问次数计算
        cache.set(cache_key, stats, timeout=60*60*24)  # 设置24小时过期时间
        
        response = self.get_response(request)
        return response