import pytest
import requests
from pages.ui_helpers import UiHelpers
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.ui_config import BASE_URL, TOKEN1, TOKEN2
from config.api_config import HEADERS
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
def cleanup_profile(driver):
    """Фикстура для полной очистки данных пользователя после теста."""
    yield
    # Блок после yield — ТЕАРДАУН (выполняется всегда, даже если тест упал!)
    print("\n[Teardown] Запуск полной очистки профиля...")
    # 1. Очищаем корзину
    try:
        cart_page = CartPage(driver)
        cart_page.clear_cart()
    except Exception as e:
        print(f"[Teardown Warning] Не удалось очистить корзину: {e}")
    # 2. Очищаем список книг / закладки
    try:
        # Передаем драйвер в класс, где объявлен clear_my_books
        books_page = BookmarkPage(driver)
        books_page.clear_my_books()
    except Exception as e:
        print(f"[Teardown Warning] Не удалось очистить список книг: {e}")
