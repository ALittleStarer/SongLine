from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

def vista_homepage(request):
    # 获取所有相册
    image_list_dir = os.path.join(settings.MEDIA_ROOT, 'vista')
    albums = [d for d in os.listdir(image_list_dir) 
             if os.path.isdir(os.path.join(image_list_dir, d))]
    
    # 处理文件上传
    if request.method == 'POST' and 'photo' in request.FILES:
        album = request.GET.get('album')
        if album:
            photos = request.FILES.getlist('photo')  # 获取多个文件
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'vista', album))
            saved_files = []
            for photo in photos:
                filename = fs.save(photo.name, photo)
                saved_files.append(filename)
            return JsonResponse({'status': 'success', 'files': saved_files})
    
    # 处理删除请求
    if request.method == 'POST' and 'delete' in request.POST:
        album = request.GET.get('album')
        filename = request.POST.get('filename')
        if album and filename:
            file_path = os.path.join(image_list_dir, album, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': '文件不存在'})
    
    # 如果请求特定相册
    album = request.GET.get('album')
    if album:
        image_dir = os.path.join(image_list_dir, album)
        images = []
        if os.path.exists(image_dir):
            for filename in sorted(os.listdir(image_dir)):
                if filename.endswith(('.jpg', '.png', '.jpeg')):
                    images.append(filename)
        current = int(request.GET.get('current', 0))
        if not images:
            current_image = None
        else:
            current = current % len(images)
            current_image = images[current]
        return render(request, 'vista/vista_album.html', {
            'album': album,
            'images': images,
            'current': current,
            'current_image': current_image,
            'total': len(images)
        })
    
    return render(request, 'vista/vista_homepage.html', {'albums': albums})


def create_album(request):
    image_list_dir = os.path.join(settings.MEDIA_ROOT, 'vista')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            album_name = data.get('name')
            if not album_name:
                return JsonResponse({'status': 'error', 'message': '相册名称不能为空'})
            
            album_path = os.path.join(image_list_dir, album_name)
            if os.path.exists(album_path):
                return JsonResponse({'status': 'error', 'message': '相册已存在'})
                
            os.makedirs(album_path)
            return JsonResponse({'status': 'success', 'album': album_name})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': '无效请求'})