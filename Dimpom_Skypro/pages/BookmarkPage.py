from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException


class BookmarkPage:

    BOOKS_COUNTER = (By.CSS_SELECTOR, 'div.header-counter__value')
    BOOK_CLEAR = (
        By.CSS_SELECTOR, 'button[data-testid-button-my-books="clearAll"]')

    CONFIRM = (By.CSS_SELECTOR, 'button[data-testid-button-dialog="confirm"]')

    EMPTY = (By.CSS_SELECTOR, 'h4[data-testid-text-stub="emptyBookmarks"]')

    def __init__(self, driver):
        self.driver = driver
        # Предполагаемый локатор для снятия закладок
        self._remove_bookmark_buttons = (
            By.CSS_SELECTOR, "button.bookmark-delete,"
            " .product-card__bookmark--active")

    def clear_my_books(self):
        """Метод удаления всех книг из закладок/избранного."""
        if "profile/bookmarks" not in self.driver.current_url:
            self.driver.get("https://chitai-gorod.ru")
        try:
            # Ищем все активные кнопки удаления закладок
            buttons = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located(
                    self._remove_bookmark_buttons))
            for button in buttons:
                if button.is_displayed():
                    button.click()
                    time.sleep(0.5)
        except TimeoutException:
            print("[Bookmark Info] Список закладок пуст, удалять нечего.")

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
