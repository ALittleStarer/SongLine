from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import logging
from django.http import JsonResponse
from dashscope import Application
import json
import random  # 添加这行导入语句

logger = logging.getLogger(__name__)

type2AppId = {
    'cat' : '011797b6cc2343ff8c9bf5c72cebe978',
    'light' : 'ec7867728c414f3f825c6af570510ec5',
    'dark' : '850b29534d7441419ed16f29807a760a',
}

def call_ai(prompt, type, max_retries=3, retry_delay=2):
    retries = 0
    while retries < max_retries:
        try:
            response = Application.call(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                app_id=type2AppId[type],
                prompt=prompt,
                timeout=60
            )

            if response.status_code == 200:
                return JsonResponse({
                    'output': {
                        'text': str(response.output)
                    }
                })
            else:
                logger.warning(f"AI服务异常，重试 {retries+1}/{max_retries}")
                
        except requests.exceptions.Timeout:
            logger.error(f"请求超时，重试 {retries+1}/{max_retries}")
        except ConnectionError:
            logger.error(f"连接异常，重试 {retries+1}/{max_retries}")
        except Exception as e:
            logger.exception("未预期的异常")
            return JsonResponse({'error': str(e)}, status=400)
            
        retries += 1
        time.sleep(retry_delay)
        
    return JsonResponse({'error': 'AI服务暂时不可用，请稍后重试'}, status=503)

def astra_home(request):
    theme = request.GET.get('theme', 'light')
    template = f'astra/astra_home_{theme}.html'
    return render(request, template, {
        'theme': theme,
        'bg_image': f'/media/astra/bg_{theme}.png'
    })

def upload_bg_image(request):
    if request.method == 'POST' and request.FILES.get('bg_image'):
        theme = request.POST.get('theme', 'dark')
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'astra'))
        filename = f'bg_{theme}.png'
        if fs.exists(filename):
            fs.delete(filename)
        fs.save(filename, request.FILES['bg_image'])
        return JsonResponse({'status': 'success', 'bg_url': f'/media/astra/{filename}'})
    return JsonResponse({'status': 'error'}, status=400)

def astra_recommend_case():
    # 这里是固定的推荐占卜问题
    return {
        'daily': '今天的运势如何？',
        'love': '我的感情会怎样发展？',
        'career': '近期工作会有哪些机遇？', 
        'finance': '未来三个月的财运如何？',
        'health': '需要注意哪些健康问题？',
        'decision': '关于XXX的选择，哪个方向更适合我？',
        'spiritual': '我当前需要领悟的人生课题是什么？'
    }

def generate_case(request):
    # 随机生成占卜问题
    if request.method == 'GET':
        theme = request.GET.get('theme', 'light')
        prompt = '请随机生成一个占卜问题, 你的回答格式为:{问题内容}, 输出不需要输出{}，也不需要加上\"问题内容:\"'
        return call_ai(prompt, theme)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def generate_prompt(case, card_names):
    # 根据占卜类型和牌面生成提示词
    prompt = f"玩家想要占卜的问题是：{case}, 请根据以下按顺序抽出来的牌面进行分析：{', '.join(card_names)}， 保持你的性格，不必太规范的解答"
    return prompt

def astra_divination(request):
    if request.method == 'GET':
        count = int(request.GET.get('count', 3))
        case = request.GET.get('case', '日常运势')
        theme = request.GET.get('theme', 'light')
        
        astra_dir = os.path.join(settings.MEDIA_ROOT, 'astra/huanxingji')
        try:
            images = [f for f in os.listdir(astra_dir) if f.endswith(('.jpg', '.png'))]
            selected = random.sample(images, min(count, len(images)))
            
            # 添加正逆位处理
            card_results = []
            for img in selected:
                position = '正位' if random.random() > 0.5 else '逆位'
                card_results.append({
                    'image': img,
                    'name': f"{img.split('.')[0]}-{position}",
                    'position': position
                })
            
            prompt = generate_prompt(case, [card['name'] for card in card_results])
            ai_response = call_ai(prompt, theme)
            
            # 从JsonResponse中提取text字段
            try:
                response_data = json.loads(ai_response.content)
                ai_text = response_data['output']['text']
                return JsonResponse({
                    'cards': card_results,
                    'interpretation': ai_text
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)


def draw_cards(request):
    """单独处理抽卡逻辑"""
    if request.method == 'GET':
        count = int(request.GET.get('count', 3))
        astra_dir = os.path.join(settings.MEDIA_ROOT, 'astra/huanxingji')
        try:
            images = [f for f in os.listdir(astra_dir) if f.endswith(('.jpg', '.png'))]
            selected = random.sample(images, min(count, len(images)))
            
            card_results = []
            for img in selected:
                position = '正位' if random.random() > 0.5 else '逆位'
                card_results.append({
                    'image': img,
                    'name': f"{img.split('.')[0]}-{position}",
                    'position': position
                })
            
            return JsonResponse({
                'cards': card_results,
                'remaining_redraws': 5  # 返回剩余重抽次数
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_divination(request):
    if request.method == 'GET':
        try:
            # 从JSON字符串解析卡牌列表
            card_names = json.loads(request.GET.get('cards', '[]'))
            case = request.GET.get('case', '日常运势')
            theme = request.GET.get('theme', 'light')  # 默认使用light主题
            
            print(f"当前主题: {theme}")  # 打印主题信息
            print(f"卡牌列表: {card_names}")  # 打印卡牌列表
            
            prompt = generate_prompt(case, card_names)
            ai_response = call_ai(prompt, theme)
            response_data = json.loads(ai_response.content)
            return JsonResponse({
                'interpretation': response_data['output']['text']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)