import allure
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage, Locator

SUCCESS_CLASS = "submission-success"


class JetpackForm:
    """Компонент формы Jetpack (используется на сайте для всех форм обратной связи).

    Успешная отправка определяется по классу 'submission-success' у тега <form>,
    ошибка поля — по атрибуту aria-invalid="true" и тексту ошибки внутри формы.
    """

    def __init__(self, page: BasePage, form_locator: Locator):
        self.page = page
        self.FORM = form_locator

    def _form_classes(self) -> list[str]:
        return (self.page.find(self.FORM).get_attribute("class") or "").split()

    def _wait_submitted(self, timeout: float) -> bool:
        try:
            # 🟡 | AI
            #
            # Вложенное ожидание: внутри lambda вызывается page.find(), у которого свой
            # WebDriverWait на DEFAULT_TIMEOUT (10 с). Если формы в DOM нет (перезагрузка,
            # перерисовка), каждый опрос висит 10 с, и is_not_submitted(3) на деле ждёт
            # 10+ с, а TimeoutException внутреннего ожидания молча превращается в «не
            # отправлена». То же в has_message и _aria_invalid. Внутри until лучше брать
            # элемент через driver.find_elements(*self.FORM) без собственного ожидания.
            self.page._wait(timeout).until(lambda _: SUCCESS_CLASS in self._form_classes())
            return True
        except TimeoutException:
            return False

    def is_submitted(self, timeout: float = 10) -> bool:
        with allure.step("Проверить, что форма успешно отправлена"):
            return self._wait_submitted(timeout)

    # 🟢 | AI
    #
    # «Не отправилась за 3 с» само по себе не доказывает отказ: при медленном ответе
    # сервера негативный тест станет зелёным. В паре с ним всегда проверяйте
    # положительный признак отказа — aria-invalid или текст ошибки (в C-N4 этого нет).
    def is_not_submitted(self, seconds: float = 3) -> bool:
        with allure.step(f"Проверить, что форма не отправилась за {seconds} с"):
            return not self._wait_submitted(seconds)

    def text(self) -> str:
        return self.page.find(self.FORM).text

    def has_message(self, message: str, timeout: float = 3) -> bool:
        with allure.step(f"Проверить, что в форме есть сообщение «{message}»"):
            try:
                self.page._wait(timeout).until(lambda _: message in self.text())
                return True
            except TimeoutException:
                return False

    def _aria_invalid(self, field: Locator) -> str:
        return self.page.find(field).get_attribute("aria-invalid") or ""

    def is_field_invalid(self, field: Locator, timeout: float = 3) -> bool:
        with allure.step("Проверить, что поле помечено как ошибочное (aria-invalid=true)"):
            try:
                self.page._wait(timeout).until(lambda _: self._aria_invalid(field) == "true")
                return True
            except TimeoutException:
                return False

    def is_field_valid(self, field: Locator, timeout: float = 3) -> bool:
        with allure.step("Проверить, что поле не помечено как ошибочное"):
            try:
                self.page._wait(timeout).until(lambda _: self._aria_invalid(field) != "true")
                return True
            except TimeoutException:
                return False
