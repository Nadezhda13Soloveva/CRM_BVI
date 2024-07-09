from django import forms
from .models import Abiturients # Импорт модели из списка Abiturients

class Abiturients_FilterForm(forms.Form):
    statuses_ = forms.MultipleChoiceField(
        choices=Abiturients.STATUSES, #  выборы из модели Abiturients
        widget=forms.CheckboxSelectMultiple,  # Отображаем как чекбоксы
        required=False # сама не знаю зачем
    )
