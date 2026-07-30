from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.ui_helpers import UiHelpers


class CartPage:

    CART = (By.CSS_SELECTOR, 'button[aria-label="Корзина"]')

    CART_PAGE = (By.CSS_SELECTOR, "div.product-cart-title__head")

    BOOKS_NAME = (By.CSS_SELECTOR, 'div.product-cart-title__head')

    CLEAR_BUTTON = (
        By.CSS_SELECTOR, 'button[data-testid-button-cart="clearAll"]')

    CLEAR_TITLE = (By.CSS_SELECTOR, 'p.cart-multiple-delete__title')

    def __init__(self, driver) -> None:
        self.driver = driver
        self.popup: UiHelpers = UiHelpers(self.driver)

    def get_cart_books(self) -> list[str]:
        """Переходит в корзину, ждёт её загрузки и возвращает названия книг."""
        self.popup.close_popup()

        self.driver.find_element(*self.CART).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_PAGE)
        )

        books_cart = self.driver.find_elements(*self.BOOKS_NAME)
        return [book.text.strip() for book in books_cart if book.text.strip()]

    def clear_cart(self) -> None:
        """Полностью очищает корзину через интерфейс сайта."""
        self.popup.close_popup()

        if self.driver.find_elements(*self.EMPTY_CART):
            return

        try:
            # Кликаем на кнопку очистки корзины
            clear_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CLEAR_BUTTON)
            )
            clear_btn.click()

            # Ждем появления UI-заглушки пустой корзины
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.EMPTY_CART)
            )
        except Exception:
            pass
