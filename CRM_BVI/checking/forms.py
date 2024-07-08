from django import forms

class SearchAbi(forms.Form):
    search_first_name = forms.CharField(help_text="Имя")
    search_second_name = forms.CharField(help_text="Фамилия")
    search_middle_name = forms.CharField(required=False, help_text="Отчество")
    search_birth_date = forms.DateField(help_text="Дата рождения", initial="DD.MM.YYYY")
    
    
