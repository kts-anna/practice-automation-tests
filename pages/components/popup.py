import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator


class Popup:
    """Компонент модального окна плагина Popup Maker (используется на сайте).

    Окно ищется по уникальному тексту внутри него, поэтому не зависит от id,
    которые могут меняться при обновлении сайта.
    """

    def __init__(self, page: BasePage, marker_text: str, name: str):
        self.page = page
        self.name = name
        self._xpath = (
            "//div[contains(@class,'pum-container')]"
            f"[contains(normalize-space(.), '{marker_text}')]"
        )
        self.CONTAINER: Locator = (By.XPATH, self._xpath)
        self.CLOSE_BUTTON: Locator = self.child(".//*[contains(@class,'pum-close')]")
        self.TITLE: Locator = self.child(".//*[contains(@class,'pum-title')]")
        self.CONTENT: Locator = self.child(".//*[contains(@class,'pum-content')]")

    def child(self, relative_xpath: str) -> Locator:
        """Локатор элемента внутри окна (relative_xpath начинается с './/')."""
        return By.XPATH, self._xpath + relative_xpath[1:]

    def is_open(self, timeout: float = 0) -> bool:
        with allure.step(f"Проверить, что окно «{self.name}» отображается"):
            return self.page.is_any_visible(self.CONTAINER, timeout)

    def is_closed(self, timeout: float | None = None) -> bool:
        with allure.step(f"Проверить, что окно «{self.name}» скрыто"):
            return self.page.wait_all_invisible(self.CONTAINER, timeout)

    def title(self) -> str:
        with allure.step(f"Получить заголовок окна «{self.name}»"):
            return self.page.find_visible(self.TITLE).text.strip()

    def content(self) -> str:
        with allure.step(f"Получить текст окна «{self.name}»"):
            return self.page.find_visible(self.CONTENT).text.strip()

    def close(self) -> None:
        with allure.step(f"Закрыть окно «{self.name}» кнопкой ×"):
            self.page.click(self.CLOSE_BUTTON)
