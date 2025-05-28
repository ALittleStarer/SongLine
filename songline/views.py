from django.shortcuts import render
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
from django.core.cache import cache
from django.http import JsonResponse
import os
from django.conf import settings

def portal_homepage(request):
    male_profile = UserProfile.objects.filter(gender='M').first()
    female_profile = UserProfile.objects.filter(gender='F').first()
    
    return render(request, 'portal_homepage.html', {
        'male_profile': male_profile,
        'female_profile': female_profile
    })

def switch_role(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        role = request.POST.get('role')
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        
        profile = UserProfile.objects.filter(gender=role).first()
        
        if profile and password == profile.view_password:
            profile.is_online = True
            profile.login_ip = ip
            profile.save()
            
            request.session['current_role'] = role
            request.session['logged_in_ip'] = ip  # 确保session中也存储IP
            request.session.modified = True
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
        
        # 清除登录缓存
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        cache.delete(f'logged_in_{ip}')
        
    auth_logout(request)
    return redirect('portal_homepage')


def music_list(request):
    music_dir = os.path.join(settings.MEDIA_ROOT, 'music')
    try:
        files = [os.path.join('/media/music/', f) for f in os.listdir(music_dir) if f.endswith('.mp3')]
        return JsonResponse(files, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)