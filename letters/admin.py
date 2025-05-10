from django.contrib import admin
from .models import Letter, UserProfile

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient_email', 'is_opened', 'opened_at')
    list_filter = ('is_opened',)
    search_fields = ('title', 'recipient_email')
    readonly_fields = ('opened_at',)
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'view_password')
    search_fields = ('user__username',)
    list_filter = ('gender',)
