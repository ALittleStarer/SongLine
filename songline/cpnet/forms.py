from django import forms
from ..models import Letter

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['title', 'recipient_email', 'content', 'image']  # 添加image字段