from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.ui_helpers import UiHelpers


class MainPage:
    SEARCH_INPUT = (By.CSS_SELECTOR, '#app-search')

    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button.search-form__button-search')

    RESULT_TEXT = (By.CSS_SELECTOR, 'h1.search-title__head')

    CATALOG = (By.CSS_SELECTOR, 'button.catalog-btn')

    CATEGORY = (
        By.XPATH, '//span[@class="categories-level-menu__'
        'item-title" and text()="Саморазвитие"]')

    SUBCATEGORY = (
        By.XPATH, '//span[@class="categories-level-menu__'
        'item-title" and text()="Цели"]')

    BOOKMARK_BUTTON = (
        By.CSS_SELECTOR, 'button.product-buttons__'
        'fav[aria-label="В закладки"]')

    MY_BOOKS = (
        By.CSS_SELECTOR, 'button[aria-label="Мои книги"]')

    MY_BOOKS_BTN = (
        By.CSS_SELECTOR, 'div.my-books-dashboard__item-title-block')

    BOOKS_COUNTER = (
        By.CSS_SELECTOR, 'div.header-counter__value')

    def __init__(self, driver) -> None:
        self.driver = driver
        self.popup: UiHelpers = UiHelpers(self.driver)

    def search_book(self, name) -> None:
        """
        Этот метод производит ввод названия книги в пое поиска,
        нажимает на кнопку поиска, и ждет
        отображения страницы с результатами.
        """

        # 1. Вводим название книги
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(name)

        # Закрытие popup если появился
        self.popup.close_popup()

        # 2. Ждем кликабельности кнопки поиска и нажимаем
        search_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.SEARCH_BUTTON
            )
        )

        # Закрытие popup если появился
        self.popup.close_popup()

        search_btn.click()

        # 3. Ждем отображения результатов
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                self.RESULT_TEXT
            )
        )

        # Закрытие popup если появился
        self.popup.close_popup()

    def open_catalog(self) -> None:
        """
        Этот метод открывает каталог с жанрами.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 1. Кликаем по каталогу
        self.driver.find_element(*self.CATALOG).click()

    def choose_category(self) -> None:
        """
        Этот метод открывает каталог подраздел с категориями жанра.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 2. Кликаем по категории
        self.driver.find_element(*self.CATEGORY).click()

    def choose_subcategory(self) -> None:
        """
        Этот метод открывает каталог подраздел с подкатегориями жанра.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 3. Кликаем по подкатегории
        self.driver.find_element(*self.SUBCATEGORY).click()

    def put_bookmarks(self, count) -> None:
        """
        Этот метод добавялет заданное количество книг с закладки.
        Защита от popup вшита в метод.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 1. Ждем, пока появятся кнопки "В закладки"
        books = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                self.BOOKMARK_BUTTON
            )
        )

        # Закрытие popup если появился
        self.popup.close_popup()

        # 2. Кликаем по первым книгам
        for book in books[:count]:
            # Ждем пока кнопка станет кликабельной
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.BOOKMARK_BUTTON))
            # Закрытие popup если появился
            self.popup.close_popup()

            # Кликаем
            book.click()

    def my_books(self) -> None:
        """
        Этот метод преходит на страницу раздела "Мои книги"
        Защита от popup вшита в метод.
        """
        # Закрытие popup если появился
        self.popup.close_popup()

        # 3. Переходим в "Мои книги"
        self.driver.find_element(*self.MY_BOOKS).click()

        # Закрытие popup если появился
        self.popup.close_popup()

        # 4. Ждем появление раздела закладок
        bookmarks = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(
                self.MY_BOOKS_BTN))

        # Закрытие popup если появился
        self.popup.close_popup()

        # 5. Кликаем по разделу закладок
        if bookmarks:
            bookmarks[1].click()
