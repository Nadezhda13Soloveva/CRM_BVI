#Добавила: проверку последних 5 лет, извлечение из названия номера в перечне и предмета, проверку на валидность
#Остался вопрос о несоответствии номеров олимпиад в перечне разных лет

import os
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Путь к Excel-файлу
abiturients_file = 'abiturients.xlsx'
bvi_file = 'bvi_mai.xlsx'

# Загрузка данных из Excel-файла
data = pd.read_excel(abiturients_file)
data = data.fillna(0)
bvi = pd.read_excel(bvi_file)

# Инициализация WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск браузера в фоновом режиме
options.add_argument('--disable-gpu')  # Отключение GPU
driver = webdriver.Chrome(options=options)

# Список для хранения результатов
abiturients = []
olimpiads = []


# Функция для выполнения поиска и сбора данных
def search_diplomas(year, fullname, firstname, middlename, birthday, birthmonth, birthyear):
    url = f'https://diploma.rsr-olymp.ru/20{year}/'
    driver.get(url)

    time.sleep(2)  # Ожидание загрузки страницы

    # Поиск и ввод данных в поля
    fullname_field = driver.find_element(By.XPATH, '//*[@id="last-name"]')
    firstname_field = driver.find_element(By.XPATH, '//*[@id="first-name"]')
    middlename_field = driver.find_element(By.XPATH, '//*[@id="middle-name"]')
    birthday_field = driver.find_element(By.XPATH, '//*[@id="bdd"]')
    birthmonth_field = driver.find_element(By.XPATH, '//*[@id="bdm"]')
    birthyear_field = driver.find_element(By.XPATH, '//*[@id="bdy"]')

    fullname_field.clear()
    firstname_field.clear()
    middlename_field.clear()
    fullname_field.send_keys(fullname)
    firstname_field.send_keys(firstname)
    middlename_field.send_keys(middlename)

    birthday_field.clear()
    birthmonth_field.clear()
    birthyear_field.clear()
    birthday_field.send_keys(birthday)
    birthmonth_field.send_keys(birthmonth)
    birthyear_field.send_keys(birthyear)
    birthyear_field.send_keys(Keys.RETURN)  # Нажатие Enter

    time.sleep(2)  # Ожидание результатов

    # Сбор данных о дипломах
    if driver.find_element(By.XPATH, '//*[@id="results"]').text == 'Ничего не найдено. Проверьте, что Вы правильно указали все данные и что год указан четырьмя цифрами.':
        print(f"Не найдено в 20{year}")
        return {}
    else:
        try:
            diplomas = {}
            page = driver.page_source

            # Подсчет количества закрывающих тегов </tr>
            rows = page.count('</tr>')

            for row in range(2, rows - 3):
                # Извлечение текста из первой ячейки второй строки
                text_way = f'//*[@id="results"]/table/tr[{row}]/td[1]'
                diploma_text_element = driver.find_element(By.XPATH, text_way)
                diploma_text = diploma_text_element.text

                # Извлечение ссылки из второй ячейки второй строки
                link_way = f'//*[@id="results"]/table/tr[{row}]/td[2]/a'
                diploma_link_element = driver.find_element(By.XPATH, link_way)
                diploma_link = diploma_link_element.get_attribute('href')

                diplomas[diploma_text] = diploma_link

            return diplomas
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
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

    is_olimp = False
    print(f"Ищем дипломы для: {full_name} {first_name} {middle_name}, Дата рождения: {'.'.join(birth)}")

    for year in range(20, 25):
        diplomas = search_diplomas(year, full_name, first_name, middle_name, birthday, birthmonth, birthyear)

        if diplomas:
            for olimp in diplomas:

                #Проверяем каждую олимпиаду на валидность: присутствие в списке олимпиад МАИ, предмет и баллы
                num = (re.search(r'№(.*?)\.', olimp)).group(1)
                topic = (re.search(r'\(\"(.*?)\"\)', olimp)).group(1)

                bvi[f'Номер в перечне на 20{year - 1}/{year} учебный год'] = bvi[
                    f'Номер в перечне на 20{year - 1}/{year} учебный год'].astype(str)

                # Используем contains с игнорированием регистра и проверяем, что значения существуют в bvi
                if f'Номер в перечне на 20{year - 1}/{year} учебный год' in bvi.columns and 'Профилирующий предмет' in bvi.columns:
                    # Найдем индексы, которые соответствуют условиям
                    index_olimp = bvi.index[
                        (bvi[f'Номер в перечне на 20{year - 1}/{year} учебный год'] == num) &
                        (bvi['Профилирующий предмет'].str.contains(topic, case=False, na=False))
                        ].tolist()

                    if index_olimp:
                        if int(row[f'ЕГЭ {topic}']) >= 75:
                            is_olimp = True
                            print(f'За 20{year} записано {olimp}')
                            # Запись результатов
                            olimpiads.append({
                                'id': id_olimpiada,
                                'abiturient_id': id_abiturient,
                                'name': olimp,
                                'year': int(f'20{year}'),
                                'diploma_file': diplomas[olimp]
                            })
                            id_olimpiada += 1


    if is_olimp:
        abiturients.append({
            'id': id_abiturient,
            'last_name': row['Фамилия'],
            'first_name': row['Имя'],
            'middle_name': row['Отчество'],
            'birth_date': '-'.join(birth[::-1]),
            'phone_number': row['Номер телефона'],
            'email': row['Электронная почта'],
            'ege_russian': int(row['ЕГЭ русский язык']),
            'ege_math': int(row['ЕГЭ математика']),
            'ege_physics': int(row['ЕГЭ физика']),
            'ege_informatics': int(row['ЕГЭ информатика']),
            'status': 'нет информации',
            'call_result': ''
        })
        id_abiturient += 1



# Закрытие WebDriver
driver.quit()

# Сохранение результатов в новый Excel-файл
abiturients_df = pd.DataFrame(abiturients)
olimpiads_df = pd.DataFrame(olimpiads)

if os.path.exists('results_abiturients.xlsx'):
    os.remove('results_abiturients.xlsx')
if os.path.exists('results_olimpiads.xlsx'):
    os.remove('results_olimpiads.xlsx')

abiturients_df.to_excel('results_abiturients.xlsx', index=False)
olimpiads_df.to_excel('results_olimpiads.xlsx', index=False)


print("Готово! Результаты сохранены в 'results_abiturients.xlsx' и 'results_olimpiads.xlsx'.")