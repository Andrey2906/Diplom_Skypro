from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class UiHelpers:

    def __init__(self, driver) -> None:
        self.driver = driver

    def close_popup(self) -> None:
        """
        Этот метод закрывает popup который
        появляется случайным образом на разных страницах.
        """
        try:
            popup = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.popmechanic-close")
                )
            )

            popup.click()

            # Ждём исчезновения overlay
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, ".popmechanic-js-clickable-overlay")))

        except TimeoutException:
            pass
