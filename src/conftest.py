import pytest
from selenium import webdriver
from appium import webdriver as appium_driver
from appium.options.android import UiAutomator2Options
from tools.main_page import MainPage
from tools.car import Car
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from time import sleep

options_otomoto = UiAutomator2Options()
options_otomoto.platform_name = "Android"
options_otomoto.device_name = "47270DLAQ0046W"  # or your device ID
options_otomoto.app_package = "pl.otomoto"
options_otomoto.app_activity = "pl.otomoto/com.fixeads.verticals.cars.startup.view.activities.SplashActivity"
options_otomoto.no_reset = True

def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        choices=["web", "mobile"],
        help="Choose platform: web or mobile",
    )


@pytest.fixture(autouse=True)
def driver(request):
    platform = request.config.getoption("--platform")
    if platform == "mobile":
        driver = appium_driver.Remote("http://127.0.0.1:4723", options=options_otomoto)
        sleep(5)
        driver.platform = platform
    else:
        driver = webdriver.Chrome()
        driver.get("https://www.otomoto.pl/")
        driver.platform = platform

    yield driver
    driver.quit()
