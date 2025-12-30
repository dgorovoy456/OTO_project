import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from appium import webdriver as appium_driver
from appium.options.android import UiAutomator2Options


def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        choices=["web", "mobile"],
        help="Choose platform: web or mobile",
    )
    parser.addoption(
        "--platforms",
        action="store",
        default="web",
        help="Choose platform: web or mobile",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run tests in headless mode",
    )


def pytest_generate_tests(metafunc):
    if "platform" in metafunc.fixturenames:
        platforms = metafunc.config.getoption("--platforms")
        platforms = platforms.split(",")
        metafunc.parametrize("platform", platforms)


@pytest.fixture(autouse=True)
def driver(request, platform):
    headless = request.config.getoption("--headless")
    if platform == "mobile":
        options_otomoto = UiAutomator2Options()
        options_otomoto.platform_name = "Android"
        options_otomoto.device_name = "47270DLAQ0046W"
        options_otomoto.app_package = "pl.otomoto"
        options_otomoto.app_activity = "pl.otomoto/com.fixeads.verticals.cars.startup.view.activities.SplashActivity"
        options_otomoto.no_reset = True
        driver = appium_driver.Remote("http://127.0.0.1:4723", options=options_otomoto)
        driver.platform = platform
    else:
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0.7103.113 Safari/537.36"
        )
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.otomoto.pl/")
        driver.platform = platform

    yield driver
    driver.quit()
