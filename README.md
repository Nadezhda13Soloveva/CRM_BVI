# МАИ CRM абитуриентов БВИ

Проект представляет собой специализированное CRM-приложение, предназначенное для обработки данных абитуриентов, поступающих БВИ.
---
<ins>Основная задача:</ins> Автоматизация котируемости олимпиад и упрощение процесса взаимодействия с абитуриентами.
---
### Индивидуальные задачи:
- [x] Настроить парсинг данных об олимпиадах абитуриента с сайта РСОШ за 2019-2024 года с сохранением ссылки на диплом
- [X] Реализовать проверку диплома РСОШ на валидность: наличие данной олимпиады в перечне МАИ этого года, соответствие профиля указанному в перечне, подтверждение баллами ЕГЭ (>= 75 баллов по профильному предмету)
- [X] Преобразовать перечень олимпиад МАИ в excel-файл и сводной информацией о номерах олимпиад в 2020-2024 годах
- [x] Разработать базу данных SQLite с информацией об абитуриентах и олимпиадах
- [x] Реализовать проверку вариантов написания ФИО с буквами Е/Ё
- [x] Реализовать преобразование ФИО в корректный формат (CAPS->Classic), а также проверку валидности ФИО и даты рождения по регулярным выражениям с предусмотрением случаев: отсутствия отчества, отчества с припиской народности, двойной фамилии, двойного имени
- [ ] Переделать парсинг хэшированием (по возможности)
