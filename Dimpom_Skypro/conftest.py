import pytest
import requests
from pages.ui_helpers import UiHelpers
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.ui_config import BASE_URL, TOKEN1, TOKEN2
from config.api_config import HEADERS


@pytest.fixture
def driver():
    driver = webdriver.Firefox()

    driver.get(BASE_URL)

    driver.add_cookie({
        "name": "access-token",
        "value": TOKEN1,
        "domain": ".chitai-gorod.ru",
        "path": "/"
    })

    driver.add_cookie({
        "name": "refresh-token",
        "value": TOKEN2,
        "domain": ".chitai-gorod.ru",
        "path": "/"
    })

    driver.get(BASE_URL)

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "span.header-controls__text"), "Vlad"
        )
    )

    driver.maximize_window()

    popup_helper = UiHelpers(driver)
    popup_helper.close_popup()

    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def session():
    s = requests.Session()

    s.headers.update(HEADERS)

    s.get("https://www.chitai-gorod.ru")

    yield s
    s.close()
