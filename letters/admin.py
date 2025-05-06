from django.contrib import admin
from .models import Letter
# Register your models here.
@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient_email', 'sent_at')
    search_fields = ('title', 'recipient_email')
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at',)
