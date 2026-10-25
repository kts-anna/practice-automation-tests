from datetime import date

import allure
import pytest

VALID_DATES = [
    pytest.param("2025-12-31", id="end_of_year"),
    pytest.param(date.today().isoformat(), id="today"),
    pytest.param("2024-02-29", id="leap_day"),
    pytest.param("2030-01-01", id="future"),
]

INVALID_DATES = [
    pytest.param("abcdef", id="letters"),
    pytest.param("31.12.2025", id="wrong_format"),
    pytest.param("2025-13-45", id="non_existent_date"),
]


@allure.epic("practice-automation.com")
@allure.feature("Календарь")
@pytest.mark.positive
class TestCalendarPositive:

    @allure.title("C-01. Страница календаря открывается, поле даты отображается")
    def test_page_opened(self, calendar_page):
        assert calendar_page.heading_text() == "Calendars"
        assert calendar_page.is_date_input_visible(), "Поле даты не отображается"

    @allure.title("C-02. У поля есть подпись и подсказка формата YYYY-MM-DD")
    def test_label_and_hint(self, calendar_page):
        text = calendar_page.form.text()
        assert calendar_page.LABEL_TEXT in text
        assert calendar_page.FORMAT_HINT in text

    @allure.title("C-03. Поле ожидает дату в формате yy-mm-dd")
    def test_date_format_attribute(self, calendar_page):
        assert calendar_page.date_format() == "yy-mm-dd"

    @allure.title("C-04. Корректная дата вводится без ошибки")
    def test_valid_date_accepted(self, calendar_page):
        calendar_page.type_date("2025-12-31")
        assert calendar_page.date_value() == "2025-12-31"
        assert calendar_page.is_date_valid(), "Корректная дата помечена как ошибочная"

    @allure.title("C-05. Форма отправляется с корректной датой {value}")
    @pytest.mark.parametrize("value", VALID_DATES)
    def test_submit_valid_date(self, calendar_page, value):
        calendar_page.type_date(value)
        calendar_page.submit()
        assert calendar_page.form.is_submitted(), f"Форма не отправилась с датой {value}"

    @allure.title("C-06. После отправки в URL есть признак отправленной формы")
    def test_url_after_submit(self, calendar_page):
        calendar_page.type_date("2025-12-31")
        calendar_page.submit()
        assert calendar_page.form.is_submitted()
        assert "contact-form-sent" in calendar_page.driver.current_url

    @allure.title("C-07. После отправки поле даты скрывается")
    def test_field_hidden_after_submit(self, calendar_page):
        calendar_page.type_date("2025-12-31")
        calendar_page.submit()
        assert calendar_page.form.is_submitted()
        assert calendar_page.is_date_input_hidden(), "Поле даты осталось на экране"

    @allure.title("C-08. Исправление неверной даты на верную снимает ошибку и позволяет отправить форму")
    def test_fix_invalid_date(self, calendar_page):
        calendar_page.type_date("abcdef")
        calendar_page.submit()
        assert calendar_page.is_date_invalid()
        calendar_page.type_date("2025-12-31")
        assert calendar_page.is_date_valid(), "Ошибка не снялась после исправления"
        calendar_page.submit()
        assert calendar_page.form.is_submitted()

    @allure.title("C-09. Поле даты можно очистить")
    def test_clear_date(self, calendar_page):
        calendar_page.type_date("2025-12-31")
        calendar_page.clear_date()
        assert calendar_page.date_value() == ""


@allure.epic("practice-automation.com")
@allure.feature("Календарь")
@pytest.mark.negative
class TestCalendarNegative:

    @allure.title("C-N1..N3. Некорректная дата «{value}» не отправляется, показывается ошибка")
    @pytest.mark.parametrize("value", INVALID_DATES)
    def test_invalid_date(self, calendar_page, value):
        calendar_page.type_date(value)
        calendar_page.submit()
        assert calendar_page.form.is_not_submitted(), f"Форма отправилась с датой «{value}»"
        assert calendar_page.is_date_invalid(), "Поле не помечено как ошибочное"
        assert calendar_page.form.has_message(calendar_page.INVALID_DATE_MESSAGE)

    @allure.title("C-N4. Форма с пустой датой не отправляется")
    def test_empty_date(self, calendar_page):
        calendar_page.type_date("")
        calendar_page.submit()
        assert calendar_page.form.is_not_submitted(), "Форма отправилась с пустым полем"
        assert "contact-form-sent" not in calendar_page.driver.current_url
