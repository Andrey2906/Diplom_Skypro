from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookPage:

    BOOK_BUTTON = (By.CSS_SELECTOR, 'button.product-preview__button')

    def __init__(self, driver) -> None:

        self.driver = driver

    def wait_for_book_page(self) -> None:
        """
        Этот метод ждет отображения карточки книги.
        """

        # 1. Ожидаем отображения карточки
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located(
                self.BOOK_BUTTON))
