import pandas as pd
import sqlite3

# # Функция для обновления таблицы в базе данных
# def update_table_from_excel(conn, df, table_name):
#     cursor = conn.cursor()
#     cursor.execute(f"DELETE FROM {table_name}")
#     df.to_sql(table_name, conn, if_exists='append', index=False)
#     conn.commit()

# Чтение данных из Excel-файлов
file_abiturients = 'results_abiturients.xlsx'
file_olimpiads = 'results_olimpiads.xlsx'
file_directions = 'directions.xlsx'

df_abiturients = pd.read_excel(file_abiturients)
df_olimpiads = pd.read_excel(file_olimpiads)
df_directions = pd.read_excel(file_directions)

# Подключение к базе данных SQLite
conn = sqlite3.connect('abiturients_olimp.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
    CREATE TABLE IF NOT EXISTS checking_abiturients (
        id INTEGER PRIMARY KEY,
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS checking_olimpiads (
        id INTEGER PRIMARY KEY,
        abiturient_id INTEGER,
        name TEXT,
        year INTEGER,
        diploma_file TEXT,
        FOREIGN KEY(abiturient_id) REFERENCES checking_abiturients(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS checking_directions (
        id INTEGER PRIMARY KEY,
        abiturient_id INTEGER,
        snils TEXT,
        sum_balls INTEGER,
        sum_balls_ege INTEGER,
        doc TEXT,
        egpu_orig TEXT,
        dormitory TEXT,
        direction_1 TEXT,
        direction_2 TEXT,
        direction_3 TEXT,
        direction_4 TEXT,
        direction_5 TEXT
    )
''')

# Загрузка данных из pandas DataFrame в таблицы базы данных SQLite
df_abiturients.to_sql('checking_abiturients', conn, if_exists='replace', index=False)
df_olimpiads.to_sql('checking_olimpiads', conn, if_exists='replace', index=False)
df_directions.to_sql('checking_directions', conn, if_exists='replace', index=False)


conn.commit()  # это включает изменения, такие как создание таблиц и вставка данных
# позволяет группировать несколько операций в одну транзакцию

# Закрытие соединения
conn.close()
