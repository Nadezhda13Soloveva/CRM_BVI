from django.shortcuts import render
from .models import Abiturients
from .forms import Abiturients_FilterForm  # Импортируем форму

def abiturients_filter_list(request):
    form = Abiturients_FilterForm(request.GET or None)  # Инициализируем форму, передавая в нее GET параметры запроса
    # Получаем всех абитуриентов из базы данных
    abiturients = Abiturients.objects.all()  # Получение всех абитуриентов

    if form.is_valid():  # Проверяем, является ли форма валидной
        # Получаем выбранные пользователем параметры из формы
        options_statuses_ = form.cleaned_data.get('options')
        # Если пользователь выбрал какие-либо параметры, фильтруем абитуриентов по этим параметрам
        if options_statuses_:
            abiturients = abiturients .filter(status__in=options_statuses_)  # фильтр по полю statuses

    # Создание контекста, который будет передан в шаблон
    context = {
        'form': form,  # Форма фильтра
        'abiturients': abiturients # Отфильтрованный список абитуриентов
    }
    # используем функцию render, чтобы отобразить шаблон product_list.html, передав в него контекст с формой и продуктами
    return render(request, 'C:\Projects\CRM_BVI-frontend\CRM_BVI-frontend\CRM_BVI\checking\abiturients_list.html', context)

# selected_statuses = ['сомневается']
# products = Abiturients.objects.all()  # Получаем все продукты
# print(products.filter(status__in=selected_statuses))  # Фильтруем продукты
