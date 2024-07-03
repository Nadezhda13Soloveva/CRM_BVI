from django.shortcuts import render
from .models import Abiturients, Olimpiads
from django.views import generic

def index(request):
    return render(request, 'index.html')
    
class Call(generic.ListView):
    model = Abiturients
