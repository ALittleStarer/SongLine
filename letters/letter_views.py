from django.shortcuts import render, redirect, get_object_or_404
from .models import Letter
from .forms import LetterForm
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.html import strip_tags
import logging
logger = logging.getLogger(__name__)

def letter_create(request):
    logger.info(f"请求方法: {request.method}")  # 添加请求方法日志
    logger.info(f"请求头: {request.headers}")  # 记录请求头信息
    if request.method == 'POST':
        logger.info("收到POST请求")  # 确认是否进入POST分支
        form = LetterForm(request.POST)
        if form.is_valid():
            letter = form.save(commit=False)
            try:
                if 'send' in request.POST:
                    html_content = letter.content.replace('\n', '<br>')
                    email = EmailMultiAlternatives(
                        letter.title,
                        strip_tags(letter.content),
                        settings.DEFAULT_FROM_EMAIL,
                        [letter.recipient_email],
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send(fail_silently=False)
                    letter.sent = True
                    letter.save()
                    return redirect('letter_success')
                else:  # 添加仅保存的明确处理
                    logger.info("here2")
                    letter.save()
                    return redirect('letter_success')
            except Exception as e:
                logger.exception("保存信件时发生严重错误")  # 这将记录完整堆栈跟踪
                return render(request, 'letters/letter_form.html', {
                    'form': form,
                    'error': f'系统错误: {str(e)}'
                })
        else:  # 添加表单无效的处理
            logger.error(f"表单验证失败: {form.errors}")
            return render(request, 'letters/letter_form.html', {
                'form': form,
                'error': '表单数据无效，请检查输入'
            })
    else:
        form = LetterForm()
    return render(request, 'letters/letter_form.html', {'form': form})

def letter_send(request, pk):
    letter = get_object_or_404(Letter, pk=pk)
    if not letter.sent:
        html_content = letter.content.replace('\n', '<br>')
        email = EmailMultiAlternatives(
            letter.title,
            strip_tags(letter.content),
            settings.DEFAULT_FROM_EMAIL,
            [letter.recipient_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        letter.sent = True
        letter.save()

    return redirect('letter_detail', pk=pk)

def letter_success(request):
    return render(request, 'letters/letter_success.html')

def letter_history(request):
    letters = Letter.objects.all().order_by('-sent_at')
    return render(request, 'letters/letter_history.html', {'letters': letters})

def letter_detail(request, pk):
    letter = get_object_or_404(Letter, pk=pk)
    prev_letter = Letter.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_letter = Letter.objects.filter(pk__gt=pk).order_by('pk').first()
    return render(request, 'letters/letter_detail.html', {
        'letter': letter,
        'prev_letter': prev_letter,
        'next_letter': next_letter
    })

def letter_delete(request, pk):
    letter = get_object_or_404(Letter, pk=pk)
    letter.delete()
    return redirect('letter_history')

def letter_comment(request, pk):
    letter = get_object_or_404(Letter, pk=pk)
    if request.method == 'POST':
        letter.comment = request.POST.get('comment', '')
        letter.save()
    return redirect('letter_detail', pk=pk)

def clear_letter_history(request):
    Letter.objects.all().delete()
    return redirect('letter_history')