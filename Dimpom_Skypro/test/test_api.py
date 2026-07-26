import pytest
import allure
from pages.BooksApi import BooksApi


# 1) Получение списка книг
@pytest.mark.api
@allure.title("Получение списка книг")
@allure.story("Книги")
def test_get_books(session):

    books_api = BooksApi(session)

    with allure.step("Отправляем GET /products с фильтром категории"):
        response = books_api.get_list_books()
        data = response.json()

    with allure.step("Проверяем статус код"):
        assert response.status_code == 200
        print(response.headers)

    with allure.step("Проверяем, что нам возвращается список книг"):
        assert "data" in data
        assert len(data["data"]) > 0


# 2) Получение данных книги по ID
@pytest.mark.api
@allure.title("Получение книги по ID")
@allure.story("ID")
def test_get_book_by_id(session):

    books_api = BooksApi(session)
    with allure.step("Отправляем GET /products с фильтром категории"):
        response = books_api.get_list_books()
        data = response.json()

    with allure.step("Ищем книгу доступную к заказу"):
        book = books_api.books_canBuy(data)

    with allure.step("Достаём ID книги из json ответа"):
        slug_id = book["attributes"]["url"].replace("product/", "")

    with allure.step(
         "Запрашиваем книгу по конкретному ID и проверяем статус код"):
        get_by_id = books_api.get_id(slug_id)
        assert get_by_id.status_code == 200


# 3) Добавление книги в раздел Закладдки по ID
@pytest.mark.api
@allure.title("Добавление книги в закладки по ID")
@allure.story("Закладки")
def test_post_bookmark(session):

    books_api = BooksApi(session)

    with allure.step("Отправляем GET /products с фильтром категории"):
        response = books_api.get_list_books()
        data = response.json()

    with allure.step("Ищем книгу доступную к заказу"):
        book = books_api.books_canBuy(data)

    with allure.step("Получаем ID книги"):
        book_id = book["attributes"]["id"]

    with allure.step("Добавляем книгу по ID в раздел Заметки"):
        bookmark = books_api.add_bookmark(book_id)
        assert bookmark.status_code == 201


# 4) Удаление книги из раздела закладки по ID
@pytest.mark.api
@allure.title("Удаление книги из закладок по ID")
@allure.story("Закладки")
def test_delete_bookmark(session, created_bookmark_id):

    books_api = BooksApi(session)

    with allure.step("Отправляем GET /products с фильтром категории"):
        response = books_api.get_list_books()
        data = response.json()

    with allure.step("Ищем книгу доступную к заказу"):
        book = books_api.books_canBuy(data)

    with allure.step("Получаем ID книги"):
        _ = book["attributes"]["id"]

    with allure.step("Удаляем книгу по ID из рездела заметки"):
        bookmark = books_api.delete_bookmark(created_bookmark_id)
        assert bookmark.status_code == 204


# 5) проверка удаления книги из раздела Закладки с невалидным ID
@pytest.mark.api
@allure.title("Удаление книги из закладок с невалидным ID")
@allure.story("Закладки")
def test_delete_invalid_bookmark(session):

    books_api = BooksApi(session)

    with allure.step("Фиксируем невалидный ID"):
        book_id = "fffffff"

    with allure.step("Удаляем книгу по невалидному ID из рездела заметки"):
        bookmark = books_api.delete_bookmark(book_id)
        assert bookmark.status_code == 404

    with allure.step("Логируем ответ консоли в отчёт"):
        allure.attach(
            f"Ответ сервера: {bookmark.text}", name="Response",
            attachment_type=allure.attachment_type.TEXT)
