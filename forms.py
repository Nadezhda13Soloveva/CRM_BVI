from django import forms
from .models import Abiturients

class SearchAbi(forms.Form):
    search_first_name = forms.CharField(help_text="Имя")
    search_second_name = forms.CharField(help_text="Фамилия")
    search_middle_name = forms.CharField(required=False, help_text="Отчество")
    search_birth_date = forms.DateField(help_text="Дата рождения", initial="DD.MM.YYYY")
    
class Comment(forms.ModelForm):
    class Meta:
        model = Abiturients
        fields = ['call_result', 'id', 'status']

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

class FilterForm(forms.Form):
    STATUS_CHOICES = Abiturients.STATUSES  # Получаем возможные значения статуса из модели Abiturients
    status = forms.MultipleChoiceField(  # Поле для выбора статуса. Используется MultipleChoiceField,
        # чтобы пользователь мог выбрать несколько статусов.
        choices= STATUS_CHOICES,
        # STATUSES=[
        #     ('Сомневается', 'Сомневается'),
        #     ('Точно будет поступать', 'Точно будет поступать'),
        #     ('Ушел в другой ВУЗ', 'Ушел в другой ВУЗ'),
        #     ('Нет информации', 'Нет информации'),
        # ]
        required=False,  # поле не явл. обязательным к заполнению
        widget=forms.CheckboxSelectMultiple,
        label = "Статус"
    )

    DIRECTIONS_CHOICES = [(key, f"Институт №{key}") for key in inst_direc.keys()]
    directions = forms.MultipleChoiceField(  #  поле для выбора направлений
        # DIRECTIONS_CHOICES = [
        #     (1, "Институт №1"),
        #     (2, "Институт №2"),
        #     (3, "Институт №3)
        # ]
        choices=DIRECTIONS_CHOICES,
        required=False,   # поле не явл. обязательным к заполнению
        widget=forms.CheckboxSelectMultiple,  #  Указывает, что поле будет отображаться с использованием виджета
        # CheckboxSelectMultiple, что позволяет выбирать несколько значений с помощью флажков.
        label="Институты"
    )
