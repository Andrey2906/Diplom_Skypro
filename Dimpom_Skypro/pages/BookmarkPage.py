from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.ui_helpers import UiHelpers


class BookmarkPage:

    BOOKS_COUNTER = (By.CSS_SELECTOR, 'div.header-counter__value')
    BOOK_CLEAR = (
        By.CSS_SELECTOR, 'button[data-testid-button-my-books="clearAll"]')

    CONFIRM = (By.CSS_SELECTOR, 'button[data-testid-button-dialog="confirm"]')

    EMPTY = (By.CSS_SELECTOR, 'h4[data-testid-text-stub="emptyBookmarks"]')

    def __init__(self, driver) -> None:
        self.driver = driver
        self.popup: UiHelpers = UiHelpers(self.driver)

    def update_counter(self) -> str:
        """
        Этот метод ждет обновления счётчика страницы "Мои книги"
        Защита от popup вшита в метод.
        """
        # Закрытие popup если появился
        self.popup.close_popup()
        counter = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.BOOKS_COUNTER
            )
        )
        return counter.text.strip()

    def clear_my_books(self) -> None:
        """
        Этот метод очищает закладки и проверет что раздел пуст.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # Поиск и нажатие на кнопку очистки
        self.driver.find_element(*self.BOOK_CLEAR).click()

        # Подтверждение очистки
        confirm = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONFIRM)
            )
        confirm.click()

        # Проверка что список пуст
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.EMPTY))
