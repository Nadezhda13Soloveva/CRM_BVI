from django.shortcuts import render
from .models import Abiturients, Olimpiads

def index(request):
    return render(request, 'index.html')
