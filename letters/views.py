from .letter_views import *
from .schedule_todo_views import *
from .vista_views import vista_homepage  # 新增导入

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    if dictionary.get(int(key)) == None:
        return "placeholder.jpg"
    return dictionary.get(int(key))

def portal_homepage(request):
    return render(request, 'letters/portal_homepage.html')