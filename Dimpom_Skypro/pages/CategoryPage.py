from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CategoryPage:

    FILTERED_PAGE = (By.CSS_SELECTOR, 'img.product-card__image')

    def __init__(self, driver) -> None:
        self.driver = driver

    def wait_for_results(self) -> None:
        """
        Этот метод ожидает прогрузки страницы по фильтрам.
        """

        # 4. Ждем отображения результатов
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                self.FILTERED_PAGE))
