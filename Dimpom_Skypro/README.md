Diplom_Skypro
Данный репозиторий содержит дипломную работу по модулю "Автоматизация тестирования на Python"
Проект автоматизирует тестирование веб-приложения Читай-Город с использованием Pytest, Allure и PageObject. Включает UI и API тесты, а также вспомогательные классы для работы с API.

🔹 Структура проекта

project/
│
├─ test/                   # Тесты
│  ├─ test_ui.py           # UI тесты
│  └─ test_api.py          # API тесты
│
├─ pages/                  # PageObject и API клиенты
│  ├─ MainPage.py
│  ├─ SearchPage.py
│  ├─ CartPage.py
│  ├─ CategoryPage.py
│  ├─ BookPage.py
│  ├─ BookmarkPage.py
│  └─ BooksApi.py          # API клиент для работы с книгами
│
├─ config/                 # Конфигурация
│  └─ api_config.py        # Base URLs, параметры запросов, токен
│
├─ requirements.txt        # Зависимости проекта
└─ README.md               # Этот файл

🔹 Технологии

Python 3.11

Pytest

Allure

Requests (для API)

Selenium / WebDriver (для UI)

PageObject Pattern

Типизация (Typing)

🔹 Установка зависимостей

python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
pip install -r requirements.txt

🔹 Настройка проекта

В файле config/api_config.py указаны:

BASE_URL_V1 — URL для API версии 1

BASE_URL_V2 — URL для API версии 2

list_books_params — параметры для получения списка книг

TOKEN — Bearer token для авторизации в API

Для UI тестов необходимо настроить WebDriver Firefox.

🔹 Запуск тестов

UI тесты:

pytest -m ui -v

API тесты:

pytest -m api -v

С генерацией Allure отчёта:

pytest -m api --alluredir=allure-results
allure serve allure-results

🔹 Структура тестов

UI тесты:

Поиск книги по названию

Открытие карточки книги

Добавление книги в корзину

Фильтрация книг по категории

Добавление книг в закладки

API тесты:

Получение списка книг

Получение данных книги по ID

Добавление книги в закладки по ID

Удаление книги из закладок по ID

Удаление книги из закладок с невалидным ID

🔹 PageObject / API клиент

UI Pages:

MainPage, SearchPage, CartPage, CategoryPage, BookPage, BookmarkPage

API клиент (BooksApi) методы:

get_list_books() — получить список книг

books_canBuy(data) — выбрать первую доступную к покупке книгу

get_book_by_slug(slug_id) — получить данные книги по slug

add_bookmark(book_id) — добавить книгу в закладки

delete_bookmark(book_id) — удалить книгу из закладок

🔹 Особенности

В API тестах реализована чистая среда: добавление и удаление книги по ID

В PageObject используются аннотации типов

UI тесты построены по PageObject Pattern для читаемости и переиспользования

Все тесты сопровождаются Allure шагами и логами

🔹 Получение Authorization Token

Для выполнения API тестов требуется Bearer Token.

Важно: токен действителен примерно 1 час. После истечения срока действия токен нужно обновить.

Шаги получения токена

Откройте сайт: https://www.chitai-gorod.ru

Нажмите F12 → вкладка Network

Найдите любой GET запрос к API, например:

https://web-agr.chitai-gorod.ru/web/api/v1/cycles?personalContent=true&page=1&perPage=12

В разделе Request Headers найдите поле:

Authorization: Bearer <token>

Скопируйте значение токена

Добавление токена в проект

Вставьте токен в файл config/api_config.py в переменную:

TOKEN = "Bearer <your_token>"

🔹 Примечание

Если API тесты начинают возвращать 403 Forbidden или 401 Unauthorized, значит токен устарел — необходимо получить новый и заменить его в api_config.py.