from django.shortcuts import render
from django.db.models import Q  #  для создания сложных запросов с логическими операторами.
from .models import Abiturients, Olimpiads, Directions
from .forms import SearchAbi, Comment, FilterForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

inst_direc = {
    1: ['24.03.04', '24.05.07', '25.03.01'],
    2: ['13.03.01', '24.05.02'],
    3: ['09.03.01', '09.03.02', '09.03.03', '09.03.04', '12.03.04', '13.03.02', '24.05.06', '27.03.04', '27.03.05'],
    4: ['10.03.01', '10.05.02', '11.05.01'],
    5: ['38.03.01', '38.03.02', '45.03.02'],
    6: ['05.03.06', '12.03.04', '24.05.01', '27.03.03', '24.05.05'],
    7: ['24.05.05', '27.03.03'],
    8: ['01.03.02', '01.03.04', '02.03.02'],
    10: ['45.03.02', '42.03.01'],
    11: ['12.03.04', '22.03.01', '22.03.02'],
}

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


def filter_view(request):
    form = FilterForm(request.POST or None)  # Создаем объект формы FilterForm. Если метод запроса POST, форма
    # заполняется данными из запроса, в противном случае форма остается пустой.
    abiturients = Abiturients.objects.all()  # Получение всех абитуриентов

    if form.is_valid():  # проверка формы на валидность
        # Извлечение данных из формы
        status = form.cleaned_data.get('status')
        directions = form.cleaned_data.get('directions')

        if status:  # фильтрация абитуриентов по статусу
            abiturients = abiturients.filter(status__in=status)

        if directions:  # фильтрация абитуриентов по направлениям
            q_objects = Q()  #  пустой объект Q, который будет использоваться для создания условий фильтрации по направлениям.
            for direction in directions:  # проходит по институтам
                direction_ids = inst_direc.get(int(direction))  # извлечения списка направлений
                if direction_ids:  # проверка, что не NONE
                    q_objects |= (Q(direction_1__in=direction_ids) |
                                  Q(direction_2__in=direction_ids) |
                                  Q(direction_3__in=direction_ids) |
                                  Q(direction_4__in=direction_ids) |
                                  Q(direction_5__in=direction_ids))

            abiturient_ids = Directions.objects.filter(q_objects).values_list('abiturient_id', flat=True)  # вывод abiturient_id
            abiturients = abiturients.filter(id__in=abiturient_ids)  # Фильтрация абитуриентов по их идентификаторам
    return render(request, 'calling.html', {'form': form, 'abiturients': abiturients})



def updata(request):
    return render(request, "updata.html")

