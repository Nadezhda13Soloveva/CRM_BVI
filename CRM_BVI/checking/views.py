from django.shortcuts import render
from .models import Abiturients, Olimpiads, Directions
from .forms import SearchAbi
from django.views import generic
from django.http import HttpResponseRedirect


def index(request):
    if request.method == "POST":
        form = SearchAbi(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["search_first_name"]
            last_name = form.cleaned_data["search_second_name"]
            middle_name = form.cleaned_data["search_middle_name"]
            birth_date = form.cleaned_data["search_birth_date"]
        else:
            return render(request, "index.html")

        abi = Abiturients.objects.filter(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            birth_date=birth_date,
        ).first()

        if abi:
            if abi.call_result==None:
            	res = str()
            else:
            	res = abi.call_result
            oli_set = abi.olimpiads_set.all()
            olimpiads = [oli.name for oli in oli_set]
            olimpiads = " | ".join(olimpiads)
            return render(
                request,
                "checking.html",
                context={
                    "name": f"{abi.first_name} {abi.last_name} {abi.middle_name}",
                    "date": abi.birth_date,
                    "phone": abi.phone_number,
                    "email": abi.email,
                    "ege_rus": abi.ege_russian,
                    "ege_m": abi.ege_math,
                    "ege_f": abi.ege_physics,
                    "ege_inf": abi.ege_informatics,
                    "status": abi.status,
                    "text": res,
                    "set": olimpiads,
                },
            )
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")


class CallList(generic.ListView):
    model = Abiturients
    context_object_name = "calling_list"
    template_name = "calling.html"


def updata(request):
    return render(request, "updata.html")

