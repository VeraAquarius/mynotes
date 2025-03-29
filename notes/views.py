from django.shortcuts import render

# Create your views here.
# notes/views.py
from .models import Note
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NoteForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

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
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})


