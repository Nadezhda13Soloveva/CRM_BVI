from django.db import models
from django.urls import reverse

class Abiturients(models.Model):
    STATUSES = [
    	('DO', 'Сомневается'),
    	('DY', 'Точно будет поступать'),
    	('DN', 'Ушел в другой ВУЗ'),
    	('NI', 'Нет информации'),
    ]
    
    # Поля
    id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
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
        return f"{self.last_name} {self.first_name} {self.middle_name},\nномер: {self.phone_number},\n{self.email}\nЕГЭ: {self.ege_russian}|{self.ege_math}|{self.ege_physics}|{self.ege_informatics}|{self.status}\n\n{self.call_result}" + "{}".format(self.birth_date.strftime('%d.%m.%Y'))
    def get_absolute_url(self):
        return reverse('abi-detail-view', args=[str(self.id)])


class Olimpiads(models.Model):

    # Поля
    id = models.IntegerField(primary_key=True)
    abiturient = models.ForeignKey(Abiturients, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    diploma_file = models.CharField(max_length=255)

    # Метаданные
    class Meta:
        pass

    # Methods
    def __str__(self):
        return f"{self.id}\n{self.name}|{self.year}\n{self.diploma_file}"
    def get_absolute_url(self):
        return reverse('olimp-detail-view', args=[str(self.id)])

class Directions(models.Model):
    # Поля
    id = models.IntegerField(primary_key=True)
    abiturient = models.ForeignKey(Abiturients, on_delete=models.CASCADE)
    snils = models.CharField(max_length=20)
    sum_balls = models.IntegerField()
    sum_balls_ege = models.IntegerField()
    doc = models.CharField(max_length=20)  # Копия или Оригинал
    egpu_orig = models.CharField(max_length=20)  # ✓ или пусто
    dormitory = models.CharField(max_length=20)  # ✓ или пусто
    direction_1 = models.CharField(max_length=20)
    direction_2 = models.CharField(max_length=20)
    direction_3 = models.CharField(max_length=20)
    direction_4 = models.CharField(max_length=20)
    direction_5 = models.CharField(max_length=20)

    # Метаданные
    class Meta:
        pass

    # Methods
    def __str__(self):
        # тут можно вывести больше информации, но пока так
        return f"{self.id}\nSNILS: {self.snils},\nСумма баллов с ИД: {self.sum_balls}\nНаправления: {self.direction_1}|{self.direction_2}|{self.direction_3}|{self.direction_4}|{self.direction_5}\n\nОбщежитие{self.dormitory}"
    
    def get_absolute_url(self):
        return reverse('direction-detail-view', args=[str(self.id)])
