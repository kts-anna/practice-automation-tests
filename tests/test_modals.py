import allure
import pytest


@allure.epic("practice-automation.com")
@allure.feature("Модальные окна")
@pytest.mark.positive
class TestModalsPositive:

    @allure.title("M-01. Страница открывается, кнопки вызова модальных окон отображаются")
    def test_page_opened(self, modals_page):
        assert modals_page.heading_text() == "Modals"
        assert modals_page.are_buttons_visible()

    @allure.title("M-02. Кнопка «Simple Modal» открывает простое окно")
    def test_simple_modal_opens(self, modals_page):
        modal = modals_page.open_simple_modal()
        assert modal.is_open(5), "Простое модальное окно не открылось"

    @allure.title("M-03. Простое окно содержит корректный заголовок и текст")
    def test_simple_modal_content(self, modals_page):
        modal = modals_page.open_simple_modal()
        assert modal.is_open(5)
        assert modal.title() == "Simple Modal"
        assert "simple modal" in modal.content().lower()

    @allure.title("M-04. Простое окно закрывается кнопкой ×")
    def test_simple_modal_closes(self, modals_page):
        modal = modals_page.open_simple_modal()
        assert modal.is_open(5)
        modal.close()
        assert modal.is_closed(), "Окно не закрылось"

    @allure.title("M-05. Простое окно можно открыть повторно после закрытия")
    def test_simple_modal_reopens(self, modals_page):
        modal = modals_page.open_simple_modal()
        assert modal.is_open(5)
        modal.close()
        assert modal.is_closed()
        modals_page.open_simple_modal()
        assert modal.is_open(5), "Окно не открылось повторно"

    @allure.title("M-06. Окно с формой открывается и содержит поля Name, Email, Message")
    def test_form_modal_opens(self, modals_page):
        modal = modals_page.open_form_modal()
        assert modal.is_open(5), "Окно с формой не открылось"
        assert modal.title() == "Modal Containing A Form"
        assert modals_page.form_fields_visible()

    @allure.title("M-07. Отправка формы со всеми заполненными полями")
    def test_form_submit_all_fields(self, modals_page):
        modals_page.open_form_modal()
        modals_page.fill_form("Ivan Petrov", "ivan@example.com", "Hello from autotest")
        modals_page.submit_form()
        assert modals_page.form.is_submitted(), "Форма не отправилась"
        assert "contact-form-sent" in modals_page.driver.current_url

    @allure.title("M-08. Отправка формы только с обязательным полем Name")
    def test_form_submit_required_only(self, modals_page):
        modals_page.open_form_modal()
        modals_page.fill_form(name="Ivan")
        modals_page.submit_form()
        assert modals_page.form.is_submitted(), "Форма не отправилась"

    @allure.title("M-09. Окно с формой закрывается кнопкой ×")
    def test_form_modal_closes(self, modals_page):
        modal = modals_page.open_form_modal()
        assert modal.is_open(5)
        modal.close()
        assert modal.is_closed(), "Окно с формой не закрылось"


@allure.epic("practice-automation.com")
@allure.feature("Модальные окна")
@pytest.mark.negative
class TestModalsNegative:

    @allure.title("M-N1. При загрузке страницы модальные окна не отображаются")
    def test_modals_hidden_on_load(self, modals_page):
        assert modals_page.are_buttons_visible()
        assert not modals_page.simple_modal.is_open()
        assert not modals_page.form_modal.is_open()

    @allure.title("M-N2. Форма не отправляется без обязательного поля Name")
    def test_form_without_name(self, modals_page):
        modal = modals_page.open_form_modal()
        modals_page.fill_form(email="ivan@example.com", message="No name")
        modals_page.submit_form()
        assert modals_page.form.is_not_submitted(), "Форма отправилась без Name"
        assert modals_page.form.is_field_invalid(modals_page.NAME_INPUT)
        assert modals_page.form.has_message(modals_page.NAME_REQUIRED_MESSAGE)
        assert modal.is_open(), "Окно с формой закрылось"

    @allure.title("M-N3. Форма не отправляется с некорректным email")
    def test_form_invalid_email(self, modals_page):
        modal = modals_page.open_form_modal()
        modals_page.fill_form(name="Ivan", email="not-an-email")
        modals_page.submit_form()
        assert modals_page.form.is_not_submitted(), "Форма отправилась с неверным email"
        assert modals_page.form.is_field_invalid(modals_page.EMAIL_INPUT)
        assert modals_page.form.has_message(modals_page.INVALID_EMAIL_MESSAGE)
        assert modal.is_open()

    @allure.title("M-N4. Полностью пустая форма не отправляется")
    def test_empty_form(self, modals_page):
        modal = modals_page.open_form_modal()
        modals_page.submit_form()
        assert modals_page.form.is_not_submitted(), "Пустая форма отправилась"
        assert modals_page.form.has_message(modals_page.NAME_REQUIRED_MESSAGE)
        assert modal.is_open()
