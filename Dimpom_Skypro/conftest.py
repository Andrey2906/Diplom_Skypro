import pytest
import requests
from pages.ui_helpers import UiHelpers
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.ui_config import BASE_URL, TOKEN1, TOKEN2
from config.api_config import HEADERS
from pages.SearchPage import SearchPage
from pages.CartPage import CartPage
from pages.BookmarkPage import BookmarkPage


@pytest.fixture
def driver():
    driver = webdriver.Firefox()

    driver.get(BASE_URL)

    driver.add_cookie({
        "name": "access-token",
        "value": TOKEN1,
        "domain": ".chitai-gorod.ru",
        "path": "/"
    })

    driver.add_cookie({
        "name": "refresh-token",
        "value": TOKEN2,
        "domain": ".chitai-gorod.ru",
        "path": "/"
    })

    driver.get(BASE_URL)

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "span.header-controls__text"), "Vlad"
        )
    )

    driver.maximize_window()

    popup_helper = UiHelpers(driver)
    popup_helper.close_popup()

    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def session():
    s = requests.Session()

    s.headers.update(HEADERS)

    s.get("https://www.chitai-gorod.ru")

    yield s
    s.close()


@pytest.fixture
def search_page(driver):
    """Фикстура инициализирует объект страницы поиска."""
    return SearchPage(driver)


@pytest.fixture
def cleanup_profile(driver):
    """Фикстура для полной очистки данных пользователя после теста.
    Переходит в целевые разделы сайта и вызывает методы объектов страниц.
    """
    yield
    # Блок Теардауна (выполняется ПОСЛЕ теста)
    print("\n[Teardown] Запуск очистки профиля через Page Objects...")

    cart_page = CartPage(driver)
    my_books_page = BookmarkPage(driver)

    # 1. Переход в корзину и очистка
    try:
        driver.get("https://www.chitai-gorod.ru/cart")
        cart_page.clear_cart()
        print("[Teardown] Метод clear_cart() успешно выполнен.")
    except Exception as e:
        print(f"[Teardown] Ошибка при очистке корзины на /cart: {e}")

    # 2. Переход в раздел книг/закладок и очистка
    try:
        driver.get("https://www.chitai-gorod.ru/my-books/bookmarks")
        my_books_page.clear_my_books()
        print("[Teardown] Метод clear_my_books() успешно выполнен.")
    except Exception as e:
        print(f"[Teardown] Ошибка при очистке 'Мои книги': {e}")
