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
@allure.title("Поиск книги по названию")
@allure.story("Поиск книги")
def test_search_by_name(search_page):
    # 1. Выполняем поиск
    search_page.search_book("Грозовый перевал")

    # 2. Получаем список найденных карточек
    results = search_page.get_search_results()
    # 3. Проверяем, что вернулось хотя бы одно совпадение
    assert len(results) > 0, "Результаты поиска пусты, хотя "
    "ожидалось совпадение"


# 2) Открытие карточки книги

@pytest.mark.ui
@allure.title("Переход на карточку книги")
@allure.story("Карточка книги")
def test_book_card(driver):

    main_page = MainPage(driver)
    search_page = SearchPage(driver)
    book_page = BookPage(driver)

    with allure.step("Выполнить поиск книги"):
        main_page.search_book("Бусидо. Кодекс самурая")

    with allure.step("Открыть первую книгу из результатов"):
        search_page.choose_first_book()

    with allure.step("Проверить что открылась карточка книги"):
        book_page.wait_for_book_page()


# 3) Добавление книг в корзину

@pytest.mark.ui
@allure.title("Добавление книг в корзину")
@allure.story("Корзина")
def test_add_books(driver):

    main_page = MainPage(driver)
    search_page = SearchPage(driver)
    cart_page = CartPage(driver)

    with allure.step("Выполнить поиск книги"):
        main_page.search_book("Высший замысел")

    with allure.step("Добавить несколько книг в корзину"):
        search_page.put_books_in_cart()

    with allure.step("Получить список книг в корзине"):
        books_in_cart = cart_page.get_cart_books()

    with allure.step("Проверить что книга добавилась"):
        assert any("Высший замысел" in title for title in books_in_cart)

    with allure.step("Очистить корзину"):
        cart_page.clear_cart()


# 4) Фильтрация книг

@pytest.mark.ui
@allure.title("Фильтрация книг по категории")
@allure.story("Каталог")
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
@allure.title("Добавление книг в закладки")
@allure.story("Избранное")
def test_bookmark_books(driver):

    main_page = MainPage(driver)
    bookmark_page = BookmarkPage(driver)

    with allure.step("Добавить книги в закладки"):
        main_page.put_bookmarks(3)

    with allure.step("Перейти в раздел Мои книги"):
        main_page.my_books()

    with allure.step("Проверить счетчик закладок"):
        current_counter = bookmark_page.update_counter()
        assert current_counter in ("2", "3")

    with allure.step("Очистить список закладок"):
        bookmark_page.clear_my_books()
