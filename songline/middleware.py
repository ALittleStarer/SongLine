from django.http import HttpResponseForbidden
from django.core.cache import cache

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        protected_paths = ['/cpnet/', '/kalam/', '/vista/']
        if any(request.path.startswith(path) for path in protected_paths):
            ip = request.META.get('REMOTE_ADDR')
            if not cache.get(f'logged_in_{ip}'):
                return HttpResponseForbidden("请先登录")
        return self.get_response(request)