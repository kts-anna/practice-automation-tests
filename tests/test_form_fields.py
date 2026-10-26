import allure
import pytest


@allure.epic("practice-automation.com")
@allure.feature("Форма (поле Message)")
@pytest.mark.positive
class TestFormFields:

    @allure.title("F-01. Поле Message заполняется списком из раздела Automation tools через запятую")
    def test_message_filled_with_tools(self, form_fields_page):
        tools = form_fields_page.get_automation_tools()
        assert tools, "Список Automation tools пуст"
        # 🟡 | AI
        #
        # Ожидаемое значение строится тем же кодом, что и проверяемое:
        # fill_message_with_tools() сам делает ", ".join(get_automation_tools()), поэтому
        # assert на следующей строке сравнивает код сам с собой. Если локатор
        # AUTOMATION_TOOLS начнёт цеплять не те <li> (или пропустит часть), тест
        # останется зелёным. Ожидаемый список инструментов стоит зафиксировать в тесте
        # явно, а проверять — значение поля Message.
        expected = form_fields_page.fill_message_with_tools()
        assert expected == ", ".join(tools)
        assert form_fields_page.message_value() == expected

    @allure.title("F-02. Форма с Message из Automation tools успешно отправляется")
    def test_submit_form_with_tools(self, form_fields_page):
        form_fields_page.fill_name("Ivan")
        form_fields_page.fill_email("ivan@example.com")
        form_fields_page.fill_message_with_tools()
        assert form_fields_page.submit_and_get_alert_text() == "Message received!"
