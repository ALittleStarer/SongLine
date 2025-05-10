from django.shortcuts import render

def chat_cat_homepage(request):
    return render(request, 'letters/chat_cat/chat_cat_homepage.html')