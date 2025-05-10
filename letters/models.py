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
    is_opened = models.BooleanField(default=False, verbose_name="是否已打开")
    opened_at = models.DateTimeField(null=True, blank=True, verbose_name="打开时间")
    opened_ips = models.JSONField(default=list)  # 存储所有查看IP和时间的记录
    last_opened_ip = models.GenericIPAddressField(null=True, blank=True)  # 最后查看IP
    
    def __str__(self):
        return f"{self.title} - {'已读' if self.is_opened else '未读'}"

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    view_password = models.CharField(max_length=100, default='LibertyIsland')  # 添加默认值
