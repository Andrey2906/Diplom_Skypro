import pytest
import allure
from pages.MainPage import MainPage
from pages.SearchPage import SearchPage
from pages.CartPage import CartPage
from pages.CategoryPage import CategoryPage
from pages.BookPage import BookPage
from pages.BookmarkPage import BookmarkPage


# 1) Поиск книги
@pytest.mark.ui
@allure.epic("UI Интернет-магазина")
@allure.feature("Поиск и Каталог")
@allure.story("Поиск книг")
@allure.title("Поиск книги по названию")
def test_search_by_name(driver, search_page):
    main_page = MainPage(driver)
    search_query = "Грозовый перевал"

    with allure.step(f"Выполнить поиск книги '{search_query}'"):
        main_page.search_book(search_query)

    with allure.step("Получить список найденных карточек"):
        results = search_page.get_search_results()

    with allure.step("Проверить, что вернулось хотя бы одно совпадение"):
        assert len(results) > 0, (
            f"Результаты поиска пусты для запроса '{search_query}', "
            f"хотя ожидалось совпадение"
        )


# 2) Открытие карточки книги
@pytest.mark.ui
@allure.epic("UI Интернет-магазина")
@allure.feature("Карточка товара")
@allure.story("Переход в карточку")
@allure.title("Переход на карточку книги")
def test_book_card(driver):
    main_page = MainPage(driver)
    search_page = SearchPage(driver)
    book_page = BookPage(driver)
    target_book = "Бусидо. Кодекс самурая"

    with allure.step(f"Выполнить поиск книги '{target_book}'"):
        main_page.search_book(target_book)

    with allure.step("Открыть первую книгу из результатов"):
        search_page.choose_first_book()

    with allure.step("Проверить что открылась карточка книги"):
        book_page.wait_for_book_page()


# 3) Добавление книг в корзину
@pytest.mark.ui
@allure.epic("UI Интернет-магазина")
@allure.feature("Корзина")
@allure.story("Добавление товаров")
@allure.title("Добавление книг в корзину")
def test_add_books(driver, cleanup_profile):  # Подключили фикстуру очистки
    main_page = MainPage(driver)
    search_page = SearchPage(driver)
    cart_page = CartPage(driver)
    target_book = "Высший замысел"

    with allure.step(f"Выполнить поиск книги '{target_book}'"):
        main_page.search_book(target_book)

    with allure.step("Добавить несколько книг в корзину"):
        search_page.put_books_in_cart()

    with allure.step("Получить список книг в корзине"):
        books_in_cart = cart_page.get_cart_books()

    with allure.step("Проверить что книга добавилась"):
        assert any(
            target_book.lower() in title.lower() for title in books_in_cart), \
            f"Книга '{target_book}' не найдена в корзине."


# 4) Фильтрация книг
@pytest.mark.ui
@allure.epic("UI Интернет-магазина")
@allure.feature("Поиск и Каталог")
@allure.story("Каталог")
@allure.title("Фильтрация книг по категории")
def test_filter(driver):
    main_page = MainPage(driver)
    category_page = CategoryPage(driver)

    with allure.step("Открыть каталог"):
        main_page.open_catalog()

    with allure.step("Выбрать категорию"):
        main_page.choose_category()

    with allure.step("Выбрать подкатегорию"):
        main_page.choose_subcategory()

    with allure.step("Проверить отображение книг"):
        category_page.wait_for_results()


# 5) Добавление книг в закладки
@pytest.mark.ui
@allure.epic("UI Интернет-магазина")
@allure.feature("Избранное")
@allure.story("Добавление в закладки")
@allure.title("Добавление книг в закладки")
def test_bookmark_books(driver, cleanup_profile):
    main_page = MainPage(driver)
    bookmark_page = BookmarkPage(driver)
    expected_count = 3

    with allure.step(f"Добавить {expected_count} книги в закладки"):
        main_page.put_bookmarks(expected_count)

    with allure.step("Перейти в раздел Мои книги"):
        main_page.my_books()

    with allure.step("Проверить счетчик закладок"):
        current_counter = bookmark_page.update_counter()
        assert int(current_counter) == expected_count, \
            f"Счетчик закладок равен {current_counter},"
        "а ожидали {expected_count}"
