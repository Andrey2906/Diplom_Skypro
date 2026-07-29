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
    Выполняет очистку напрямую через драйвер,
    не используя удаленные методы классов.
    """
    yield
    # Блок Теардауна (выполняется ПОСЛЕ теста)
    print("\n[Teardown] Запуск прямой очистки профиля от сайд-эффектов...")
    # 1. Прямая очистка Корзины через UI
    try:
        driver.get("https://chitai-gorod.ru")
        # Локатор кнопки очистки корзины на сайте
        clear_cart_locator = (
            By.CSS_SELECTOR, "button.cart-clean-button, .button-clear")
        # Ожидаем кнопку и кликаем по ней напрямую через драйвер
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(clear_cart_locator)
        )
        button.click()
        print("[Teardown] Корзина успешно очищена.")
    except Exception as e:
        print(f"[Teardown Info] Очистка корзины пропущена. Причина: {e}")

    # 2. Прямая очистка Закладок через UI
    try:
        driver.get("https://chitai-gorod.ru")
        # Локатор активных иконок удаления/сердечек в списке закладок
        remove_bookmark_locator = (
            By.CSS_SELECTOR, "button.bookmark-delete,"
            " .product-card__bookmark--active")
        # Ищем все элементы закладок и кликаем по ним напрямую через драйвер
        buttons = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located(remove_bookmark_locator)
        )
        for button in buttons:
            if button.is_displayed():
                button.click()
        print("[Teardown] Все закладки успешно удалены.")
    except Exception as e:
        print(f"[Teardown Info] Очистка закладок пропущена. Причина: {e}")
