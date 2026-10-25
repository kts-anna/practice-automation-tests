import allure
from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage
from pages.components.jetpack_form import JetpackForm
from pages.components.popup import Popup


class ModalsPage(BasePage):
    URL = f"{BASE_URL}/modals/"

    SIMPLE_MODAL_BUTTON = (By.XPATH, "//*[self::button or self::a][normalize-space()='Simple Modal']")
    FORM_MODAL_BUTTON = (By.XPATH, "//*[self::button or self::a][normalize-space()='Form Modal']")

    NAME_REQUIRED_MESSAGE = "This field is required."
    INVALID_EMAIL_MESSAGE = "Please enter a valid email address"

    def __init__(self, driver):
        super().__init__(driver)
        self.simple_modal = Popup(self, "a simple modal", "Simple Modal")
        self.form_modal = Popup(self, "Modal Containing A Form", "Form Modal")
        fm = self.form_modal
        self.NAME_INPUT = fm.child(".//input[@type='text'][contains(@id,'name')]")
        self.EMAIL_INPUT = fm.child(".//input[@type='email']")
        self.MESSAGE_INPUT = fm.child(".//textarea[not(contains(@name,'ak_'))]")
        self.SUBMIT_BUTTON = fm.child(".//button[@type='submit']")
        self.form = JetpackForm(self, fm.child(".//form"))

    def are_buttons_visible(self) -> bool:
        with allure.step("Проверить наличие кнопок Simple Modal и Form Modal"):
            return (self.is_any_visible(self.SIMPLE_MODAL_BUTTON, self.timeout)
                    and self.is_any_visible(self.FORM_MODAL_BUTTON, self.timeout))

    @allure.step("Нажать кнопку «Simple Modal»")
    def open_simple_modal(self) -> Popup:
        self.click(self.SIMPLE_MODAL_BUTTON)
        return self.simple_modal

    @allure.step("Нажать кнопку «Form Modal»")
    def open_form_modal(self) -> Popup:
        self.click(self.FORM_MODAL_BUTTON)
        self.form_modal.is_open(5)
        return self.form_modal

    def form_fields_visible(self) -> bool:
        with allure.step("Проверить, что поля Name, Email, Message и кнопка Submit видны"):
            return all(self.is_any_visible(loc, self.timeout) for loc in
                       (self.NAME_INPUT, self.EMAIL_INPUT, self.MESSAGE_INPUT, self.SUBMIT_BUTTON))

    @allure.step("Заполнить форму: name='{name}', email='{email}', message='{message}'")
    def fill_form(self, name: str = "", email: str = "", message: str = "") -> None:
        if name:
            self.type_text(self.NAME_INPUT, name)
        if email:
            self.type_text(self.EMAIL_INPUT, email)
        if message:
            self.type_text(self.MESSAGE_INPUT, message)

    @allure.step("Нажать Submit в форме модального окна")
    def submit_form(self) -> None:
        self.click(self.SUBMIT_BUTTON)
