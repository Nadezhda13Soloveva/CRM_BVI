import sqlite3
import pandas as pd

abiturients_file = 'results_abiturients.xlsx'  # таблица с контактами абитуриентов
olimpiads_file = 'results_olimpiads.xlsx'  # таблица со сведениями об олимпиаде
directions_file = 'directions.xlsx'  # таблица с направлениями, СНИЛСОМ, копия или ориг, общага

# Загрузка данных из эксель-файла
abiturients = pd.read_excel(abiturients_file)
olimpiads = pd.read_excel(olimpiads_file)
directions = pd.read_excel(directions_file)

# Подключение к базе данных SQLite
conn = sqlite3.connect('abiturients_olimp-directions.db')  # Итого наша БД будет состоять из 3 таблиц
c = conn.cursor()

# Создание таблицы, если она еще не существует
c.execute('''
CREATE TABLE IF NOT EXISTS Abiturients (  # таблица с контктами абитуры
    id INTEGER,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    birth_date DATE,
    phone_number TEXT,
    email TEXT,
    ege_russian INTEGER,
    ege_math INTEGER,
    ege_physics INTEGER,
    ege_informatics INTEGER,
    status TEXT,
    call_result TEXT
)
''')

c.execute('''  # таблица сведений об олимпиадах
CREATE TABLE IF NOT EXISTS Olimpiads (
    id INTEGER,
    abiturient_id INTEGER,
    name TEXT,
    year INTEGER,
    diploma_file TEXT
)
''')
c.execute('''  # таблица с направлениями, СНИЛСОМ, копия или ориг, общага
CREATE TABLE IF NOT EXISTS Directions (
    id INTEGER,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    birth_date DATE,
    snils TEXT,
    sum_balls INTEGER,
    sum_balls_ege INTEGER,
    doc TEXT,
    egpu_orig TEXT,
    dormitory TEXT,
    priority_1 TEXT,
    priority_2 TEXT,
    priority_3 TEXT,
    priority_4 TEXT,
    priority_5 TEXT,
)
''')


# Список словарей для проверки и обновления
abiturients = abiturients.to_dict('records')
olimpiads = olimpiads.to_dict('records')
directions = directions.to_dict('records')


# Функция для обновления или добавления информации об абитуриенте
def update_or_insert_bd(bd, entrant):
    # Проверка наличия информации о человеке в базе данных
    c.execute(f'SELECT * FROM {bd} WHERE id = ?', (entrant['id'],))
    result = c.fetchone()
    if result:
        # Если информация о человеке содержится, но значения ключей отличаются
        if result != tuple(entrant.values()):
            columns = ', '.join(f"{k} = ?" for k in entrant.keys())
            values = list(entrant.values()) + [entrant['id']]
            c.execute(f'UPDATE {bd} SET {columns} WHERE id = ?', values)
    else:
        # Если информация о человеке не содержится, добавление новой записи
        placeholders = ', '.join('?' * len(entrant))
        columns = ', '.join(entrant.keys())
        c.execute(f'INSERT INTO {bd} ({columns}) VALUES ({placeholders})', list(entrant.values()))


# Проход по списку словарей и обновление базы данных
for bd in (abiturients, olimpiads, directions):
    for entrant in bd:
        if bd == abiturients:
            update_or_insert_bd('Abiturients', entrant)
        elif bd == directions:
            update_or_insert_bd('Olimpiads', entrant)
        else:
            update_or_insert_bd('Directions', entrant)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
