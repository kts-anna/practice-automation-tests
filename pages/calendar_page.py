import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import BASE_URL
from pages.base_page import BasePage
from pages.components.jetpack_form import JetpackForm


class CalendarPage(BasePage):
    URL = f"{BASE_URL}/calendars/"

    _INPUT_XPATH = ("//input[contains(@class,'jp-contact-form-date') "
                    "or contains(@name,'selectorenteradate')]")
    DATE_INPUT = (By.XPATH, _INPUT_XPATH)
    FORM = (By.XPATH, f"{_INPUT_XPATH}/ancestor::form")
    SUBMIT_BUTTON = (By.XPATH, f"{_INPUT_XPATH}/ancestor::form//button[@type='submit']")

    LABEL_TEXT = "Select or enter a date"
    FORMAT_HINT = "YYYY-MM-DD"
    INVALID_DATE_MESSAGE = "Please enter a valid date."

    def __init__(self, driver):
        super().__init__(driver)
        self.form = JetpackForm(self, self.FORM)

    def is_date_input_visible(self) -> bool:
        with allure.step("Проверить, что поле даты отображается"):
            return self.is_any_visible(self.DATE_INPUT, self.timeout)

    def is_date_input_hidden(self, timeout: float = 5) -> bool:
        with allure.step("Проверить, что поле даты скрыто"):
            return self.wait_all_invisible(self.DATE_INPUT, timeout)

    @allure.step("Получить ожидаемый формат даты (атрибут data-format)")
    def date_format(self) -> str:
        return self.find(self.DATE_INPUT).get_attribute("data-format") or ""

    @allure.step("Ввести в поле даты «{text}» и убрать фокус с поля")
    def type_date(self, text: str) -> None:
        self.click(self.DATE_INPUT)
        field = self.find(self.DATE_INPUT)
        field.clear()
        if text:
            field.send_keys(text)
        field.send_keys(Keys.TAB)

    @allure.step("Очистить поле даты")
    def clear_date(self) -> None:
        field = self.find(self.DATE_INPUT)
        field.send_keys(Keys.END)
        field.send_keys(Keys.BACKSPACE * len(field.get_property("value") or ""))

    @allure.step("Получить значение поля даты")
    def date_value(self) -> str:
        return self.get_value(self.DATE_INPUT)

    @allure.step("Нажать кнопку Submit")
    def submit(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    def is_date_invalid(self) -> bool:
        return self.form.is_field_invalid(self.DATE_INPUT)

    def is_date_valid(self) -> bool:
        return self.form.is_field_valid(self.DATE_INPUT)
