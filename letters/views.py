from .letter_views import *
from .schedule_todo_views import *
from .vista_views import vista_homepage  # 新增导入

from django.template.defaulttags import register
from django.http import StreamingHttpResponse
from dashscope import Application
import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Letter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password, check_password
import random  # 添加这行导入语句
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect
from .models import UserProfile  # 添加这行导入
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')
            
            # 调用AI服务获取响应
            response = Application.call(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                app_id="011797b6cc2343ff8c9bf5c72cebe978",
                prompt=prompt
            )
            
            if response.status_code == 200:
                return JsonResponse({
                    'output': {
                        'text': str(response.output)  # 根据实际响应结构调整
                    }
                })
            else:
                return JsonResponse({'error': 'AI服务调用失败'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@register.filter
def get_item(dictionary, key):
    if dictionary.get(int(key)) == None:
        return "placeholder.jpg"
    return dictionary.get(int(key))

def portal_homepage(request):
    male_profile = UserProfile.objects.filter(gender='M').first()
    female_profile = UserProfile.objects.filter(gender='F').first()
    
    return render(request, 'letters/portal_homepage.html', {
        'male_profile': male_profile,
        'female_profile': female_profile
    })

def gamejam_home(request):
    games = [
        {
            'name': 'Concern50', 
            'url': 'concern50_game',  # 本地游戏路由
            'is_external': False
        },
        # 可以在这里添加更多游戏
    ]
    return render(request, 'games/gamejam_home.html', {'games': games})

def concern50_game(request):
    return render(request, 'games/concern50.html')

def switch_role(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # 获取对应性别的用户配置
        profile = UserProfile.objects.filter(gender=role).first()
        
        if profile and password == profile.view_password:  # 简单比较，实际应该用check_password
            profile.is_online = True  # 新增：更新在线状态
            profile.save()  # 新增：保存状态
            request.session['current_role'] = role
            return redirect('portal_homepage')
        return HttpResponseForbidden("密码错误")
    return HttpResponse(status=405)  # 如果不是POST请求返回405

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            profile = user.profile
            profile.is_online = True
            profile.save()
            return redirect('portal_homepage')

def logout_view(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.is_online = False
        profile.save()
    auth_logout(request)
    return redirect('portal_homepage')