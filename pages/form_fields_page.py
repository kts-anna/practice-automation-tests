import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL
from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    URL = f"{BASE_URL}/form-fields/"

    NAME_INPUT = (By.ID, "name-input")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_INPUT = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    AUTOMATION_TOOLS = (By.XPATH, "//label[contains(normalize-space(.), 'Automation tools')]"
                                  "/following::ul[1]/li")

    @allure.step("Получить список инструментов из раздела Automation tools")
    def get_automation_tools(self) -> list[str]:
        self.find(self.AUTOMATION_TOOLS)
        tools = [item.text.strip() for item in self.find_all(self.AUTOMATION_TOOLS)]
        tools = [t for t in tools if t]
        allure.attach("\n".join(tools), name="Automation tools",
                      attachment_type=allure.attachment_type.TEXT)
        return tools

    @allure.step("Заполнить поле Message списком инструментов через запятую")
    def fill_message_with_tools(self) -> str:
        text = ", ".join(self.get_automation_tools())
        self.type_text(self.MESSAGE_INPUT, text)
        return text

    @allure.step("Ввести имя «{name}»")
    def fill_name(self, name: str) -> None:
        self.type_text(self.NAME_INPUT, name)

    @allure.step("Ввести email «{email}»")
    def fill_email(self, email: str) -> None:
        self.type_text(self.EMAIL_INPUT, email)

    @allure.step("Получить значение поля Message")
    def message_value(self) -> str:
        return self.get_value(self.MESSAGE_INPUT)

    @allure.step("Нажать Submit и прочитать текст alert")
    def submit_and_get_alert_text(self) -> str:
        self.click(self.SUBMIT_BUTTON)
        alert = self._wait().until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text
