from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Letter(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()  # 这里将存储包含图片的HTML内容
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(default=timezone.now)
    sent = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='letter_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class Schedule(models.Model):
    day = models.IntegerField(verbose_name='星期几', help_text='1 - 7 表示周一到周日')
    start = models.CharField(max_length=5, verbose_name='开始时间', help_text='格式：HH:MM')
    end = models.CharField(max_length=5, verbose_name='结束时间', help_text='格式：HH:MM')
    title = models.CharField(max_length=200, verbose_name='标题')

    def __str__(self):
        return self.title


class Todo(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
