from django.shortcuts import render

# Create your views here.
# notes/views.py
from .models import Note
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NoteForm

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