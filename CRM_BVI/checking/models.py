from django.db import models
from django.urls import reverse

class Abiturients(models.Model):
    STATUSES = [
    	('DO', 'Сомневается'),
    	('DY', 'Точно поступает'),
    	('DN', 'Точно не поступает'),
    	('NI', 'Нет информации'),
    ]
    
    # Поля
    abiturient_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15, unique_for_date=True)
    email = models.CharField(max_length=100, unique_for_date=True)
    ege_russian = models.IntegerField()
    ege_math = models.IntegerField()
    ege_physics = models.IntegerField()
    ege_informatics = models.IntegerField()
    status = models.CharField(max_length=50,choices=STATUSES)
    call_result = models.TextField(null=True, blank=True)

    # Метаданные
    class Meta:
        pass

    # Methods
    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return f"{self.last_name} {self.first_name} {self.middle_name} {self.birth_date}г.р.,\nномер: {self.phone_number},\n{self.email}\nЕГЭ: {self.ege_russian}|{self.ege_math}|{self.ege_physics}|{self.ege_informatics}|{self.status}\n\n{self.call_result}"


class Olympiads(models.Model):

    # Поля
    olympiads_id = models.IntegerField(primary_key=True)
    abiturient_id = models.ForeignKey('Abiturients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    diploma_file = models.CharField(max_length=255)

    # Метаданные
    class Meta:
        pass

    # Methods
    def __str__(self):
        return f"{self.abiturient_id}\n{self.name}|{self.year}\n{self.diploma_file}"
