from django.shortcuts import render
from .models import Abiturients, Directions
from .forms import AbiturientsFilterForm

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


def filter_abiturients(request):
    if request.method == 'GET':
        form = AbiturientsFilterForm(request.GET)  # Создаем экземпляр формы и передаем данные из запроса GET.
        # Если данных нет, то передаем None.
        abiturients = Abiturients.objects.all()  # получение всех объектов Abiturients

        if form.is_valid():  # проверка валидности формы:
            status = form.cleaned_data.get('status')
            direction_keys = form.cleaned_data.get('direction_key')
            #  содержат выбранные значения статусов и ключей направлений соотв

            if status:  # если пользователь выбрал статусы, фильтруем абитуриентов по этим статусам
                abiturients = abiturients.filter(status__in=status)

            if direction_keys:  # если пользователь выбрал ключи направлений
                direction_codes = [] # Создаем список direction_codes, который содержит
                # все направления для выбранных ключей.
                for key in direction_keys:
                    direction_codes.extend(inst_direc[int(key)])
                # Фильтруем абитуриентов по каждому из полей направлений (direction_1, direction_2, и т.д.),
                # используя объединение (|) запросов для получения абитуриентов, которые имеют хотя бы одно из
                # выбранных направлений.
                abiturients = abiturients.filter(directions__direction_1__in=direction_codes) | \
                              abiturients.filter(directions__direction_2__in=direction_codes) | \
                              abiturients.filter(directions__direction_3__in=direction_codes) | \
                              abiturients.filter(directions__direction_4__in=direction_codes) | \
                              abiturients.filter(directions__direction_5__in=direction_codes)
                # abiturients = abiturients.filter(
                #     models.Q(directions__direction_1__in=direction_codes) |
                #     models.Q(directions__direction_2__in=direction_codes) |
                #     models.Q(directions__direction_3__in=direction_codes) |
                #     models.Q(directions__direction_4__in=direction_codes) |
                #     models.Q(directions__direction_5__in=direction_codes)
                # ).distinct()
                # Метод distinct() используется для устранения дубликатов в результате объединения запросов
    return render(request, 'abiturients_list.html', {'form': form, 'abiturients': abiturients})
