from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SearchPage:

    FIRST_BOOK = (
        By.CSS_SELECTOR, 'img.product-card__'
        'image[alt="Бусидо. Кодекс самурая"]')

    BOOKS_CARDS = (
        By.CSS_SELECTOR, 'button.product-buttons__main-action')

    CART_COUNTER = (
        By.CSS_SELECTOR, 'div[data-testid-indicator-header="cartCounter"]')

    def __init__(self, driver):
        self.driver = driver
        # Локатор карточек товара в результатах поиска
        self._product_cards = (By.CSS_SELECTOR, "article.product-card")

    def get_search_results(self):
        """Ожидает появление карточек книг на
        странице поиска и возвращает их список."""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self._product_cards)
            )
        except TimeoutException:  # Исправлено
            print("[SearchPage Error] Кнопки добавления "
                  "в корзину не найдены на странице результатов")

    def choose_first_book(self) -> None:
        """
        Этот метод выбирает первую книгу
        на странице с результатами и переходт на её карточку.
        Защита от popup вшита в метод.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 1. Выбираем 1 книгу
        cards = self.driver.find_elements(*self.FIRST_BOOK)

        # Клик по 1 книгу из списка
        cards[0].click()

    def put_books_in_cart(self) -> None:
        """
        Этот метод выбирает 3 книги
        на странице поиска и добавляяет их в корзину.
        Защита от popup вшита в метод.
        """

        # 1.Ждем отображения книг
        books = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.BOOKS_CARDS))

        # Закрытие popup если появился
        self.popup.close_popup()

        # 2. Выбираем 3 в корзину
        for book in books[:3]:
            book.click()

        # 3. Ждем обновления счетчика корзины
        WebDriverWait(self.driver, 15).until(
            EC.text_to_be_present_in_element(
                self.CART_COUNTER, "3"))
