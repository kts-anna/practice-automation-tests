import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.ads_page import AdsPage
from pages.calendar_page import CalendarPage
from pages.form_fields_page import FormFieldsPage
from pages.modals_page import ModalsPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=["chrome", "firefox"], help="Браузер для запуска тестов")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Запуск браузера без графического интерфейса")


def _create_driver(browser: str, headless: bool):
    # Selenium Manager (встроен в Selenium 4.6+) сам скачивает актуальный драйвер
    if browser == "firefox":
        options = FirefoxOptions()
        options.page_load_strategy = "eager"
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
        return driver

    options = ChromeOptions()
    options.page_load_strategy = "eager"
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    with allure.step(f"Запустить браузер {browser}"):
        drv = _create_driver(browser, headless)
    yield drv
    with allure.step("Закрыть браузер"):
        drv.quit()


@pytest.fixture
def calendar_page(driver) -> CalendarPage:
    return CalendarPage(driver).open()


@pytest.fixture
def modals_page(driver) -> ModalsPage:
    return ModalsPage(driver).open()


@pytest.fixture
def ads_page(driver) -> AdsPage:
    return AdsPage(driver).open()


@pytest.fixture
def form_fields_page(driver) -> FormFieldsPage:
    return FormFieldsPage(driver).open()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """При падении теста прикладывает к Allure-отчёту скриншот, URL и HTML страницы."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return
    try:
        allure.attach(drv.get_screenshot_as_png(), name="Скриншот при ошибке",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(drv.current_url, name="URL страницы",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(drv.page_source, name="HTML страницы",
                      attachment_type=allure.attachment_type.HTML)
    except Exception as error:  # например, открыт alert
        allure.attach(str(error), name="Не удалось сделать скриншот",
                      attachment_type=allure.attachment_type.TEXT)


def pytest_sessionfinish(session):
    """Записывает информацию об окружении в Allure (вкладка Environment)."""
    alluredir = session.config.getoption("--alluredir", default=None)
    if not alluredir:
        return
    import os
    import platform
    import selenium
    from config import BASE_URL
    os.makedirs(alluredir, exist_ok=True)
    with open(os.path.join(alluredir, "environment.properties"), "w", encoding="utf-8") as f:
        f.write(f"Browser={session.config.getoption('--browser')}\n")
        f.write(f"Headless={session.config.getoption('--headless')}\n")
        f.write(f"Base.URL={BASE_URL}\n")
        f.write(f"Python={platform.python_version()}\n")
        f.write(f"Selenium={selenium.__version__}\n")
        f.write(f"OS={platform.system()} {platform.release()}\n")
