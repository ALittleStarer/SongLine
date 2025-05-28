from django.shortcuts import render, get_object_or_404
from ..models import Book
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage 
from django.shortcuts import redirect

def book_list(request):
    books = Book.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'books/list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # 添加文件路径验证
    file_path = os.path.join(settings.MEDIA_ROOT, book.file.name)
    if not os.path.exists(file_path):
        return render(request, 'books/error.html', {'error': '文件不存在'})

    # 根据文件类型处理内容显示
    content = None
    if book.format in ['md', 'txt']:
        content = book.parsed_content
    elif book.format == 'pdf':
        content = f'{settings.MEDIA_URL}{book.file.url}'
    
    return render(request, 'books/detail.html', {
        'book': book,
        'content': content
    })

def book_editor(request, pk=None):
    book = None  # 初始化book变量
    if request.method == 'POST':
        # 获取或创建书籍对象
        book = get_object_or_404(Book, pk=pk) if pk else None
        
        # 处理文件上传
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # 验证文件类型
            ext = uploaded_file.name.split('.')[-1].lower()
            if ext not in ['md', 'txt', 'pdf', 'docx']:
                return JsonResponse({'error': '不支持的文件格式'}, status=400)
            
            # 保存文件
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'books'))
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            # 更新书籍信息
            if not book:
                book = Book()  # 确保对象被创建
            book.title = request.POST.get('title', '未命名书籍')
            book.file.name = f'books/{filename}'
            book.format = ext
            book.save()
            
            # 可选：解析文本内容（示例处理markdown）
            if ext in ['md', 'txt']:
                with open(os.path.join(fs.location, filename), 'r') as f:
                    book.parsed_content = f.read()
                    book.save()
            
            return redirect('book_detail', pk=book.pk)
    
    # GET请求处理保持不变
    return render(request, 'books/editor.html', {'book': book})