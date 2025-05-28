from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse  # 添加这行导入
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.utils import timezone  # Add this import
import logging

logger = logging.getLogger(__name__)

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