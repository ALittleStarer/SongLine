from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Document
from django.contrib.auth.models import User

@login_required
def doc_editor(request, doc_id=None):
    doc = get_object_or_404(Document, pk=doc_id) if doc_id else None
    
    if request.method == 'POST':
        if not doc:
            doc = Document(author=request.user)
        doc.title = request.POST.get('title', '未命名文档')
        doc.content = request.POST.get('content', '')
        doc.save()
        return redirect('doc_view', doc_id=doc.id)
    
    return render(request, 'document/editor.html', {'doc': doc})

def doc_view(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    return render(request, 'document/view.html', {'doc': doc})