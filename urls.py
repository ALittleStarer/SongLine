# ... existing code ...
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... 其他 URL 配置 ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ... existing code ...