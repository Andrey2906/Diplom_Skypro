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
        """
        Переходит в корзину, ждёт её загрузки и возвращает названия книг.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        self.driver.find_element(*self.CART).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_PAGE)
        )

        books_cart = self.driver.find_elements(*self.BOOKS_NAME)
        return [book.text for book in books_cart]

    def clear_cart(self) -> None:
        """
        Этот метод производит очистку корзины от занесенных книг.
        Защита от popup вшита в метод.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 1. Чистим корзину
        cart_cleaner = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.CLEAR_BUTTON
                )
            )

        cart_cleaner.click()

        # 2. Ждем завершения очиски
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                self.CLEAR_TITLE, "Корзина очищена"))
