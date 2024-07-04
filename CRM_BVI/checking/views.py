from django.shortcuts import render
from .models import Abiturients, Olimpiads, Directions
from django.views import generic
from django.http import HttpResponseRedirect

def index(request):
    if request.method == 'POST':
        search = request.POST.get('checking')
        abi = Abiturient.objects.filter(first_name__icontains=search) & Abiturient.objects.filter(
            second_name__icontains=search) & Abiturient.objects.filter(
            middle_name__icontains=search) & Abiturient.objects.filter(
            date_birth__icontains=search) 
        
        first_name = "AAA"
    	second_name = "BB"
    	middle_name = "C"
    	date_birth = "01.01.2000"
    	phone_number = "=77777777"
    	email = "a@g"
    	ege_rus = 90
    	ege_m = 100
    	ege_f = 123
    	ege_inf = 456
    	status = "No informations"
    	text = "This is very hard abi"
    
    	return render(request,
    'checking.html',
    context={"name": f"{first_name} {second_name} {middle_name}", "date": date_birth, "phone": phone_number, "email": email, "ege_rus": ege_rus, "ege_m": ege_m, "ege_f": ege_f, "ege_inf": ege_inf, "status": status, "text": text}
    )
    else:
    	return render(request, 'index.html')
    
class CallList(generic.ListView):
    model = Abiturients
    context_object_name = 'calling_list'
    template_name = 'calling.html'

def index(request):
    return render(request, 'updata.html')
