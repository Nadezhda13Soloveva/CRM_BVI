import sqlite3
import pandas as pd

abiturients_file = 'results_abiturients.xlsx'
olimpiads_file = 'results_olimpiads.xlsx'

# Загрузка данных из Excel-файла
abiturients = pd.read_excel(abiturients_file)
olimpiads = pd.read_excel(olimpiads_file)

# Подключение к базе данных SQLite
conn = sqlite3.connect('abiturients_olimp.db')
c = conn.cursor()

# Создание таблицы, если она еще не существует
c.execute('''
CREATE TABLE IF NOT EXISTS Abiturients (
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

c.execute('''
CREATE TABLE IF NOT EXISTS Olimpiads (
    id INTEGER,
    abiturient_id INTEGER,
    name TEXT,
    year INTEGER,
    diploma_file TEXT
)
''')

# Список словарей для проверки и обновления
abiturients = abiturients.to_dict('records')
olimpiads = olimpiads.to_dict('records')


# Функция для обновления или добавления информации о абитуриенте

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
for bd in (abiturients, olimpiads):
    for entrant in bd:
        if bd == abiturients:
            update_or_insert_bd('Abiturients', entrant)
        else:
            update_or_insert_bd('Olimpiads', entrant)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
