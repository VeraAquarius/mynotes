from django.shortcuts import render

# Create your views here.
# notes/views.py
from .models import Note,Tag
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteForm,TagForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def welcome(request):
    return HttpResponse("欢迎来到我的笔记应用！")

def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'notes/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'notes/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/index.html', {'notes': notes})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # 将当前用户关联到笔记
            note.save()
            form.save_m2m()  # 保存多对多关系
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})

# @login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('index')  # 非创建者重定向
    if request.method == 'POST':
        note.delete()
        return redirect('index')
    return render(request, 'notes/delete_note.html', {'note': note})


def search_notes(request):
    query = request.GET.get('q', '')
    notes = Note.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    return render(request, 'notes/search_results.html', {'notes': notes, 'query': query})


def advanced_search(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    tags = request.GET.get('tags')

    notes = Note.objects.all()

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if start_date:
        notes = notes.filter(created_at__gte=start_date)
    if end_date:
        notes = notes.filter(created_at__lte=end_date)
    if tags:
        notes = notes.filter(tags__name__in=tags).distinct()

    all_tags = Tag.objects.all()

    return render(request, 'notes/advanced_search.html', {
        'notes': notes,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'selected_tags': tags,
        'all_tags': all_tags
    })


@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TagForm()
    return render(request, 'notes/create_tag.html', {'form': form})



