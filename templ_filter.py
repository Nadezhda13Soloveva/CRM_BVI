inst_direc = {  # берём только бюджет
    1: ['24.03.04', '24.05.07', '25.03.01'],
    2: ['13.03.01', '24.05.02'],
    3: ['09.03.01', '09.03.02', '09.03.03', '09.03.04', '12.03.04', '13.03.02', '24.05.06', '27.03.04', '27.03.05'],
    4: ['10.03.01', '10.05.02', '11.05.01'],
    5: ['38.03.01', '38.03.02', '45.03.02'],  # 38.03.01&38.03.02=38.03.01, тк направление включает в себя 2 кода
    6: ['05.03.06', '12.03.04', '24.05.01', '27.03.03', '24.05.05'],
    7: ['24.05.05', '27.03.03'],
    8: ['01.03.02', '01.03.04', '02.03.02'],  # 01.03.02&01.03.04=01.03.02, тк направление включает в себя 2 кода
    10: ['45.03.02', '42.03.01'],
    11: ['12.03.04', '22.03.01', '22.03.02'],  # 22.03.01&22.03.02=22.03.01, тк направление включает в себя 2 кода
}

class Enrollee:
    def __init__(self, first_name, last_name, middle_name, birth_date, directions, status, choice):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birth_date = birth_date
        self.directions = directions  # список кодов-направлений абитуриента
        self.status = status  # False: не обзвонен, если True, то обзвонен
        self.choice = choice  # None, если не обзвонен, да, нет или думает, если обзвонен

    # def __eq__(self, other):  # для сравнения и пересечения объектов класса по обзвон не обзвон
    #     if isinstance(other, Enrollee):
    #         return (self.status) == (other.status)
    #     return False

    def display_info(self):
        print(f"Фамилия: {self.last_name}")
        print(f"Имя: {self.first_name}")
        print(f"Отчество: {self.middle_name}")
        print(f"Дата рождения: {self.birth_date}")
        print(f"Выбранные направления: {self.directions}")
        print(f"Флажок 1: {self.status}")
        print(f"Флажок 2: {self.choice}")

# Пример
new_student1 = Enrollee(
    first_name="Иванов",
    last_name="Иван",
    middle_name="Иванович",
    birth_date="01.01.2006",
    directions=['01.03.02', '01.03.04'],
    status=True,
    choice='Думает'
)

new_student2 = Enrollee(
    first_name="Мария",
    last_name="Вербицкая",
    middle_name="Владимировна",
    birth_date="01.01.2007",
    directions=['22.03.01', '09.03.01'],
    status=False,
    choice=None
)
# print(new_student1.display_info())

abiturients = [new_student1, new_student2]
selected_directions = [3, 7]

# Сортировка по институтам
def institut(enrollee):
    for i in selected_directions:  # проходимся по выбранным ключам
        for j in inst_direc[i]:  # проходимся по значению ключа словаря
            if j in enrollee.directions:
                return True
    return False

def call(enrollee):
    if enrollee.status == True:
        return True

def not_call(enrollee):
    if enrollee.status == False:
        return False

filtred_Enrollees_inst = filter(institut, abiturients)  # (по какому принципу сортируется каждый объект, массив объектов
filtred_Enrollees_inst = list(filtred_Enrollees_inst)
print('\nОтфильтрованные только по институтам:')
print(*(i.display_info() for i in filtred_Enrollees_inst))

print('\nОтфильтрованные только по "обзвонен"')
filtred_Enrollees_called = filter(call, abiturients)
filtred_Enrollees_called = list(filtred_Enrollees_called)
print(*(i.display_info() for i in filtred_Enrollees_called))

# и т.д и т.п
filtred_Enrollees_not_called = filter(not_call, abiturients)  # только "не обзвонен"
filtred_Enrollees_not_called = list(filtred_Enrollees_not_called)

print('\nОтфильтрованные только по институтам и "обзвонен"')

# Можно использовать numpy, быстро, тк написано на С, но! нужно будет реализовывать в классе Enrollee методы сравнения
# (их будет много)
# obs_inst = np.intersect1d(filtred_Enrollees_inst, filtred_Enrollees_called)
# print(*(i.display_info() for i in obs_inst))


# Для статуса после обзвона filtred_Enrollees_called должно быть верно и по 3 подстатусам или сделать пересеченями?

instituts_buttons = [0, 0, 0, 1, 0, 1, 0, 1, 0]  # 9 подкнопок, т.к 9 институтов
# 1 - кнопка активирована, 0 - нет

# result_button = False  # Пока пользователь не нажал кнопку показать результаты
# selected_directions = []
# while result_button != True:
#     key = int(input())  # пользователь выбирает ключи
#     selected_directions += inst_direc[key]




# Как реализовать с БД django
# https://chatgpt.com/share/36a02056-2549-4e8f-b0e3-547221a16f42


# Сортировка по институтам
# def institut(**kwargs):  # ф-ия принимает бесконечное кол-во именованных аргументов в виде словаря
#     for key, value in kwargs.items():
#         for i in range(abiturients):
#             for j in value:
#                 if value[j] in abiturients[i].directions:
#                     print('Тут должен быть нужный объект-студент')
#                     break
