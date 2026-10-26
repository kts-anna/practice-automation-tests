import allure
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        StaleElementReferenceException, TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_TIMEOUT

Locator = tuple[str, str]


class BasePage:
    """Базовый класс Page Object: общие действия и ожидания."""

    URL: str = ""
    HEADING: Locator = (By.CSS_SELECTOR, "h1")

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout: float | None = None) -> WebDriverWait:
        return WebDriverWait(
            self.driver,
            self.timeout if timeout is None else timeout,
            ignored_exceptions=[StaleElementReferenceException],
        )

    def open(self):
        with allure.step(f"Открыть страницу {self.URL}"):
            self.driver.get(self.URL)
        return self

    # ---------- поиск ----------
    def find(self, locator: Locator, timeout: float | None = None) -> WebElement:
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator, timeout: float | None = None) -> WebElement:
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    # ---------- действия ----------
    def scroll_to(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def click(self, locator: Locator, timeout: float | None = None) -> None:
        element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
        self.scroll_to(element)
        # 🟡 | AI
        #
        # Запасной клик через JavaScript прячет дефекты: если кнопку перекрывает overlay
        # или другое окно, пользователь кликнуть не сможет, а тест пройдёт. Через этот
        # метод идут все клики проекта, включая закрытие рекламы и модалок. Лучше убрать
        # fallback и пусть тест падает; если где-то JS-клик действительно нужен — отдельный
        # явный метод js_click() с объяснением, почему.
        try:
            element.click()
        except ElementClickInterceptedException:
            with allure.step("Обычный клик перехвачен, выполняем клик через JavaScript"):
                self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.find_visible(locator)
        self.scroll_to(element)
        if clear:
            element.clear()
        element.send_keys(text)

    # 🟢 | AI
    #
    # press_escape нигде не используется — можно удалить.
    def press_escape(self, locator: Locator) -> None:
        self.find(locator).send_keys(Keys.ESCAPE)

    def get_value(self, locator: Locator) -> str:
        return self.find(locator).get_property("value") or ""

    # ---------- проверки состояния ----------
    def is_any_visible(self, locator: Locator, timeout: float = 0) -> bool:
        """Есть ли среди найденных элементов хотя бы один видимый (ждём до timeout сек)."""
        try:
            self._wait(timeout).until(
                lambda d: any(e.is_displayed() for e in d.find_elements(*locator))
            )
            return True
        except TimeoutException:
            return False

    def wait_all_invisible(self, locator: Locator, timeout: float | None = None) -> bool:
        """Ждёт, пока все элементы по локатору станут невидимыми (или исчезнут)."""
        try:
            self._wait(timeout).until(
                lambda d: not any(e.is_displayed() for e in d.find_elements(*locator))
            )
            return True
        except TimeoutException:
            return False

    def stays_invisible(self, locator: Locator, seconds: float) -> bool:
        """True, если элемент ни разу не стал видимым в течение seconds секунд."""
        return not self.is_any_visible(locator, seconds)

    @allure.step("Получить заголовок страницы")
    def heading_text(self) -> str:
        return self.find_visible(self.HEADING).text.strip()
