import allure
from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage
from pages.components.popup import Popup


class AdsPage(BasePage):
    URL = f"{BASE_URL}/ads/"

    INTRO_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'An ad will appear in')][not(*)]")
    # Затемнение (overlay), внутри которого лежит рекламное окно
    AD_OVERLAY = (By.XPATH, "//div[contains(@class,'pum-overlay')]"
                            "[.//div[contains(@class,'pum-container')][contains(., 'I am an ad')]]")
    AD_APPEAR_TIMEOUT = 15

    def __init__(self, driver):
        super().__init__(driver)
        self.ad = Popup(self, "I am an ad", "Реклама")

    def is_intro_visible(self) -> bool:
        with allure.step("Проверить текст о скором появлении рекламы"):
            return self.is_any_visible(self.INTRO_TEXT, self.timeout)

    @allure.step("Дождаться появления рекламного окна")
    def wait_for_ad(self) -> bool:
        return self.ad.is_open(self.AD_APPEAR_TIMEOUT)

    def is_overlay_visible(self, timeout: float = 0) -> bool:
        with allure.step("Проверить, что затемнение рекламы отображается"):
            return self.is_any_visible(self.AD_OVERLAY, timeout)

    def is_overlay_hidden(self, timeout: float = 5) -> bool:
        with allure.step("Проверить, что затемнение рекламы скрыто"):
            return self.wait_all_invisible(self.AD_OVERLAY, timeout)

    # 🟢 | AI
    #
    # Шаг называется «…под рекламой», но этот же метод вызывается в A-07 уже после
    # закрытия рекламы — в отчёте шаг вводит в заблуждение.
    @allure.step("Кликнуть по заголовку страницы под рекламой")
    def click_heading(self) -> None:
        self.find_visible(self.HEADING).click()
