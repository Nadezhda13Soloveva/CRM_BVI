import re
import hashlib
import requests
import os
import pandas as pd


# Путь к Excel-файлу
abiturients_file = 'abiturients.xlsx'
bvi_file = 'bvi_mai.xlsx'

# Загрузка данных из Excel-файла
data = pd.read_excel(abiturients_file)
data.iloc[:, :6] = data.iloc[:, :6].fillna('')
data.iloc[:, 6:] = data.iloc[:, 6:].fillna(0)
bvi = pd.read_excel(bvi_file)

# Список для хранения результатов
abiturients = []
olimpiads = []

# Функция проверки вариантов написания имён с е/ё
def generate_word_variants(word):
    # Генерирует варианты слова с заменой 'Е' на 'Ё' не более одного раза."""
    variants = [word]
    indices = [i for i, letter in enumerate(word) if letter == 'Е']

    for idx in indices:
        variant_list = list(word)
        variant_list[idx] = 'Ё'
        variants.append(''.join(variant_list))

    indices = [i for i, letter in enumerate(word) if letter == 'е']

    for idx in indices:
        variant_list = list(word)
        variant_list[idx] = 'ё'
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


def format_name(name):
    if " " in name:
        name = name.split(" ")
        name = " ".join([i.capitalize() for i in name])
    elif "-" in name:
        name = name.split("-")
        name = "-".join([i.capitalize() for i in name])
    else:
        name = name.capitalize()
    return name


def validate_name_and_date(last_name, first_name, middle_name, birth_date):
    # Регулярное выражение для имени (Фамилия Имя Отчество), включая "-" и пробелы (не более 1 пробела)
    name_pattern = re.compile(r"^[А-Яа-яЁёA-Za-z-]+( [А-Яа-яЁёA-Za-z-]+)?$")

    # Регулярное выражение для даты (ГГГГ-ММ-ДД)
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    # Проверка фамилии, имени и отчества по регулярному выражению
    last_name_match = name_pattern.match(last_name)
    first_name_match = name_pattern.match(first_name)
    middle_name_match = True if middle_name == "" else bool(name_pattern.match(middle_name))

    # Проверка даты по регулярному выражению
    date_match = date_pattern.match(birth_date)

    # Убедимся, что все части имени и дата корректны
    return (bool(last_name_match) and
            bool(first_name_match) and
            bool(middle_name_match) and
            bool(date_match))


id_abiturient = id_olimpiada = 1
# Проход по всем записям в Excel-файле
for index, row in data.iterrows():
    last_name = format_name(row['Фамилия'])
    first_name = format_name(row['Имя'])
    middle_name = format_name(row['Отчество'])
    birth = row['Дата рождения'].strftime('%d.%m.%Y').split('.')
    bdd = birth[0]
    bdm = birth[1]
    bdy = birth[2]

    if len(bdd) == 1:
        bdd = f'0{bdd}'
    if len(bdm) == 1:
        bdm = f'0{bdm}'

    birth = '-'.join([bdy, bdm, bdd])
    is_valid = validate_name_and_date(last_name, first_name, middle_name, birth)

    if is_valid and any(row[col] >= 75 for col in ['ЕГЭ русский язык', 'ЕГЭ математика', 'ЕГЭ физика', 'ЕГЭ информатика']):
        is_olimp = False
        print(f"Ищем дипломы для: {last_name} {first_name} {middle_name}, Дата рождения: {birth}")

        #сюда проверка на е-ё
        name_variants = generate_name_variants(' '. join([last_name, first_name, middle_name]))

        for name in name_variants:
            print(name)
            to_hash = ' '.join([name, birth])

            while "  " in to_hash:
                to_hash = to_hash.replace("  ", " ")

            hashed = hashlib.sha256(to_hash.encode()).hexdigest()

            for year in range(20, 25):
                diplomas = search_diplomas(year, hashed)
                if diplomas:
                    print(year, diplomas)










