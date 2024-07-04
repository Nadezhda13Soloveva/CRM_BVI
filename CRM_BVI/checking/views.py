from django.shortcuts import render
from .models import Abiturients, Olimpiads, Directions
from django.views import generic

def index(request):
    return render(request, 'index.html')
    
class CallList(generic.ListView):
    model = Abiturients
    context_object_name = 'calling_list'
    template_name = 'calling.html'
