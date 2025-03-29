from django.shortcuts import render

# Create your views here.
# notes/views.py
from django.shortcuts import render
# from .models import Note

def index(request):
    # notes = Note.objects.all()
    # return render(request, 'notes/index.html', {'notes': notes})
    return render(request, 'notes/index.html', {'notes': "hello world"})