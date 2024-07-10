from django import forms
from .models import Abiturients

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

class AbiturientsFilterForm(forms.Form):
    STATUSES = Abiturients.STATUSES  # Получаем возможные значения статуса из модели Abiturients
    status = forms.MultipleChoiceField(  # Поле для выбора статуса. Используется MultipleChoiceField,
        # чтобы пользователь мог выбрать несколько статусов.
        choices=STATUSES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    DIRECTIONS_CHOICES = [(key, f"Институт №{key}") for key in inst_direc.keys()]
    direction_key = forms.MultipleChoiceField(  #  поле для выбора направлений
        # DIRECTIONS_CHOICES = [
        #     (1, "Институт №1"),
        #     (2, "Институт №2"),
        #     (3, "Институт №3)
        # ]
        choices=DIRECTIONS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
