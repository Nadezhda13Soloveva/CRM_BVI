from django.db import models
# Здесь находятся описания таблиц в базе данных

# models.Autofield может быть только одно
class Enrollee(models.Model):
    enrollee_id = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    ege_ru = models.IntegerField()
    ege_math = models.IntegerField()
    ege_ph = models.IntegerField()
    ege_inf = models.IntegerField()
    status_choices = [('нет информации'), ('Думает'), ('Точно да'), ('Точно нет')]
    comment = models.CharField(max_length=1500)  # для комментария, мб позже можно увеличить

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class OlimpiadResult(models.Model):
    result_id = models.IntegerField()
    enrollee_id = models.IntegerField()
    olimp_name = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    event_date = models.CharField(max_length=500)  # ссылка на олимпиаду

    def __str__(self):
        return f"{self.enrollee_id} - {self.olimp_name} ({self.year})"


# Количество экзаменов переменно. В исходной эксель-таблице должно быть ограничение