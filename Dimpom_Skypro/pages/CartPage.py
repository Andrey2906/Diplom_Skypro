from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CartPage:

    CART = (By.CSS_SELECTOR, 'button[aria-label="Корзина"]')

    CART_PAGE = (By.CSS_SELECTOR, "div.product-cart-title__head")

    BOOKS_NAME = (By.CSS_SELECTOR, 'div.product-cart-title__head')

    CLEAR_BUTTON = (
        By.CSS_SELECTOR, 'button[data-testid-button-cart="clearAll"]')

    CLEAR_TITLE = (By.CSS_SELECTOR, 'p.cart-multiple-delete__title')

    def __init__(self, driver):
        self.driver = driver
        # Локатор кнопки "Очистить корзину" или удаления товара
        self._clear_cart_button = (
            By.CSS_SELECTOR, "button.cart-clean-button, .button-clear")

    def clear_cart(self):
        """Метод полной очистки корзины для теардауна."""
        # Переходим в корзину напрямую, если мы еще не там
        if "cart" not in self.driver.current_url:
            self.driver.get("https://chitai-gorod.ru")
        try:
            # Ожидаем кнопку очистки корзины
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self._clear_cart_button)
            )
            button.click()
        except TimeoutException:
            print("[Cart Info] "
                  "Корзина уже пуста или кнопка очистки не найдена.")

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
