from django.shortcuts import render

# Create your views here.
# notes/views.py
from django.shortcuts import render
from .models import Note
from django.http import HttpResponse

def welcome(request):
    return HttpResponse("欢迎来到我的笔记应用！")

def index(request):
    notes = Note.objects.all()
    return render(request, 'notes/index.html', {'notes': notes})