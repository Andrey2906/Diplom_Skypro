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
        """Ждет обновления счётчика страницы 'Мои книги'."""
        self.popup.close_popup()
        counter = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.BOOKS_COUNTER)
        )
        return counter.text.strip()

    def clear_my_books(self) -> None:
        """Полностью очищает список закладок, если они присутствуют."""
        self.popup.close_popup()

        # Если заглушка "Пусто" уже отображается, сразу выходим
        if self.driver.find_elements(*self.EMPTY):
            return

        try:
            # Нажимаем «Очистить всё»
            clear_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.BOOK_CLEAR)
            )
            clear_btn.click()

            # Подтверждаем удаление в модальном окне
            confirm_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONFIRM)
            )
            confirm_btn.click()

            # Ждем появления заглушки, подтверждающей успешное удаление
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.EMPTY)
            )
        except Exception:
            pass
