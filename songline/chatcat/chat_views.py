from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import logging
from django.http import JsonResponse
from dashscope import Application
import json

def chat_cat_homepage(request):
    return render(request, 'chat_cat/chat_cat_homepage.html')

def ai_chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt')

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