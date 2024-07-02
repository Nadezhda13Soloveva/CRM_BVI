import os
import re
import pandas as pd
import requests
import hashlib

# Путь к Excel-файлу
abiturients_file = 'abiturients.xlsx'
bvi_file = 'bvi_mai.xlsx'

# Загрузка данных из Excel-файла
data = pd.read_excel(abiturients_file)
data.iloc[:, :6] = data.iloc[:, :6].fillna('-')
data.iloc[:, 6:] = data.iloc[:, 6:].fillna(0)
bvi = pd.read_excel(bvi_file)

# Список для хранения результатов
abiturients = []
olimpiads = []


# Функция проверки вариантов написания имён с е/ё
def generate_word_variants(word):
    """Генерирует варианты слова с заменой 'Е' на 'Ё' не более одного раза."""
    variants = [word]
    indices = [i for i, letter in enumerate(word) if letter == 'Е']

    for idx in indices:
        variant_list = list(word)
        variant_list[idx] = 'Ё'
        variants.append(''.join(variant_list))

    return variants


def generate_name_variants(name):
    words = name.split()
    all_word_variants = [generate_word_variants(word) for word in words]

    combined_variants = []

    def combine(words_variants, current_combination, index):
        if index == len(words_variants):
            combined_variants.append(' '.join(current_combination))
            return

        for variant in words_variants[index]:
            combine(words_variants, current_combination + [variant], index + 1)

    combine(all_word_variants, [], 0)

    return combined_variants


# Функция для генерации хэша
def generate_hash(last_name, first_name, middle_name, birth_date):
    namestring = f"{last_name} {first_name} {middle_name} {birth_date}"
    return hashlib.sha256(namestring.encode()).hexdigest()


# Функция для выполнения поиска и сбора данных
def search_diplomas(year, hashed):
    url = f'https://diploma.rsr-olymp.ru/files/rsosh-diplomas-static/compiled-storage-20{year}/by-person-released/{hashed}/codes.js'
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text
        return page_content
    elif response.status_code == 404:
        print(f"Не найдено в 20{year}")
        return {}
    else:
        print(f"Ошибка при запросе: {response.status_code}")
        return {}


id_abiturient = id_olimpiada = 1
# Проход по всем записям в Excel-файле
for index, row in data.iterrows():
    full_name = row['Фамилия']
    first_name = row['Имя']
    middle_name = row['Отчество']
    birth = row['Дата рождения'].strftime('%d.%m.%Y').split('.')
    birthday = birth[0]
    birthmonth = birth[1]
    birthyear = birth[2]

    if any(row[col] >= 75 for col in ['ЕГЭ русский язык', 'ЕГЭ математика', 'ЕГЭ физика', 'ЕГЭ информатика']):
        is_olimp = False
        print(f"Ищем дипломы для: {full_name} {first_name} {middle_name}, Дата рождения: {'.'.join(birth)}")

        # сюда проверка на е-ё
        name_variants = generate_name_variants(' '.join([full_name, first_name, middle_name]))

        for name in name_variants:
            print(name)
            full_name, first_name, middle_name = name.split(" ")
            hashed = generate_hash(full_name, first_name, middle_name, f'{birthday}.{birthmonth}.{birthyear}')
            for year in range(20, 25):
                page_content = search_diplomas(year, hashed)
                if page_content:
                    print(page_content)

