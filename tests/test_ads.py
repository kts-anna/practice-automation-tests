import allure
import pytest
from selenium.common.exceptions import ElementClickInterceptedException


@allure.epic("practice-automation.com")
@allure.feature("Рекламные окна")
@pytest.mark.positive
class TestAdsPositive:

    @allure.title("A-01. Страница открывается, отображается текст о появлении рекламы")
    def test_page_opened(self, ads_page):
        assert ads_page.heading_text() == "Ads"
        assert ads_page.is_intro_visible()

    @allure.title("A-02. Рекламное окно появляется автоматически")
    def test_ad_appears(self, ads_page):
        assert ads_page.wait_for_ad(), "Реклама не появилась"

    @allure.title("A-03. Рекламное окно содержит текст «I am an ad.»")
    def test_ad_content(self, ads_page):
        assert ads_page.wait_for_ad()
        assert "I am an ad" in ads_page.ad.content()

    @allure.title("A-04. В рекламном окне есть кнопка закрытия")
    def test_ad_has_close_button(self, ads_page):
        assert ads_page.wait_for_ad()
        assert ads_page.is_any_visible(ads_page.ad.CLOSE_BUTTON, 2)

    @allure.title("A-05. Пока реклама открыта, страница затемнена")
    def test_overlay_shown_with_ad(self, ads_page):
        assert ads_page.wait_for_ad()
        assert ads_page.is_overlay_visible()

    @allure.title("A-06. Рекламное окно закрывается кнопкой ×")
    def test_ad_closes(self, ads_page):
        assert ads_page.wait_for_ad()
        ads_page.ad.close()
        assert ads_page.ad.is_closed(), "Реклама не закрылась"

    @allure.title("A-07. После закрытия рекламы затемнение пропадает, страница доступна")
    def test_page_available_after_close(self, ads_page):
        assert ads_page.wait_for_ad()
        ads_page.ad.close()
        assert ads_page.is_overlay_hidden()
        ads_page.click_heading()  # не должно быть перехвата клика
        assert ads_page.heading_text() == "Ads"

    @allure.title("A-08. После закрытия реклама не появляется снова в течение 10 секунд")
    def test_ad_not_reappear(self, ads_page):
        assert ads_page.wait_for_ad()
        ads_page.ad.close()
        assert ads_page.ad.is_closed()
        assert ads_page.stays_invisible(ads_page.ad.CONTAINER, 10), "Реклама появилась снова"


@allure.epic("practice-automation.com")
@allure.feature("Рекламные окна")
@pytest.mark.negative
class TestAdsNegative:

    @allure.title("A-N1. Реклама не показывается сразу после загрузки страницы")
    def test_ad_not_shown_immediately(self, ads_page):
        # 🟡 | AI
        #
        # Проверка с timeout=0 сразу после open() при page_load_strategy=eager идёт до
        # того, как скрипты Popup Maker вообще успели отработать. Тест пройдёт, даже
        # если реклама показывается мгновенно после загрузки. Надёжнее проверить, что
        # окно не появилось за несколько секунд меньше заявленной задержки:
        # ads_page.stays_invisible(ads_page.ad.CONTAINER, 3).
        assert not ads_page.ad.is_open(), "Реклама показалась без задержки"

    @allure.title("A-N2. Пока реклама открыта, клик по странице перехватывается окном")
    def test_click_blocked_by_ad(self, ads_page):
        assert ads_page.wait_for_ad()
        with pytest.raises(ElementClickInterceptedException):
            ads_page.click_heading()

    @allure.title("A-N3. После закрытия кнопка × рекламы больше не отображается")
    def test_close_button_hidden_after_close(self, ads_page):
        assert ads_page.wait_for_ad()
        ads_page.ad.close()
        assert ads_page.wait_all_invisible(ads_page.ad.CLOSE_BUTTON, 5)
