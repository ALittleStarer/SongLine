from django.shortcuts import render
from ..models import Schedule, Todo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_protect
def cpnet_homepage(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'add':
                day = request.POST.get('day')
                start = request.POST.get('start')
                end = request.POST.get('end')
                title = request.POST.get('title')
                schedule = Schedule.objects.create(day=day, start=start, end=end, title=title)
                return JsonResponse({'success': True, 'id': schedule.id})
            elif action == 'edit':
                index = request.POST.get('index')
                schedule = Schedule.objects.get(id=index)
                schedule.day = request.POST.get('day')
                schedule.start = request.POST.get('start')
                schedule.end = request.POST.get('end')
                schedule.title = request.POST.get('title')
                schedule.save()
                return JsonResponse({'success': True})
            elif action == 'delete':
                index = request.POST.get('index')
                Schedule.objects.get(id=index).delete()
                return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    schedules = Schedule.objects.all()
    return render(request, 'kalam/kalam.html', {'schedules': schedules})

@csrf_exempt
def schedule_operations(request):
    if request.method == 'GET':
        schedules = list(Schedule.objects.all().values())
        return JsonResponse(schedules, safe=False)
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            
            if action == 'delete':
                try:
                    schedule_id = request.POST.get('index')
                    schedule = Schedule.objects.get(id=schedule_id)
                    schedule.delete()
                    return JsonResponse({'success': True})
                except Schedule.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Schedule not found'})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': str(e)})
            
            elif action == 'add':
                schedule = Schedule.objects.create(
                    day=request.POST.get('day'),
                    start=request.POST.get('start'),
                    end=request.POST.get('end'),
                    title=request.POST.get('title')
                )
                return JsonResponse({'success': True, 'id': schedule.id})
                
            elif action == 'edit':
                schedule = Schedule.objects.get(id=request.POST.get('index'))
                schedule.day = request.POST.get('day')
                schedule.start = request.POST.get('start')
                schedule.end = request.POST.get('end')
                schedule.title = request.POST.get('title')
                schedule.save()
                return JsonResponse({'success': True})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def todo_operations(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_todo':
            todo = Todo.objects.create(
                title=request.POST.get('title')
            )
            return JsonResponse({'success': True, 'id': todo.id})
        elif action == 'delete_todo':
            Todo.objects.filter(id=request.POST.get('id')).delete()
            return JsonResponse({'success': True})
    
    todos = Todo.objects.values('id', 'title')
    return JsonResponse(list(todos), safe=False)