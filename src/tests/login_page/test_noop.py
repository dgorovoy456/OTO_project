from tools.helper import hw
from appium import webdriver
from time import sleep
from tools.main_page import MainPage, MainAndroidPage
from tools.car import Car
import os
from appium.options.android import UiAutomator2Options

# options_main_page = UiAutomator2Options()
# options_main_page.platform_name = "Android"
# options_main_page.device_name = "47270DLAQ0046W"  # or your device ID
# options_main_page.unlock_type = "password"
# options_main_page.unlock_key = "qwerty450"

# options_calculator = UiAutomator2Options()
# options_calculator.platform_name = "Android"
# options_calculator.device_name = "47270DLAQ0046W"  # or your device ID
# options_calculator.app_package = "com.google.android.calculator"
# options_calculator.app_activity = "com.google.android.calculator/com.android.calculator2.Calculator"
# options_calculator.no_reset = True


def enter_main_page(driver):
    # driver = webdriver.Remote("http://127.0.0.1:4723", options=options_main_page)
    driver.press_keycode(3)
    sleep(1)


def launch_calculator(driver):
    driver.activate_app("com.google.android.calculator")


class TestLoginPage:
    def test_that_import_working(self, driver):
        volvo_car = Car("Subaru", "Legacy", "2015")
        main_page = MainPage(driver)
        cars = main_page.get_cars(volvo_car)

        # main_page = MainAndroidPage(driver)
        # main_page.set_brand_model()
        # main_page = MainPage(driver)
        # cars = main_page.search_car(volvo_car)
        for car in cars:
            print("###############################")
            print(car)
            print("###############################")
        # print(f"#################{driver.platform}################")
        assert 1 + 1 == 2
        # self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options_main_page)
        # enter_main_page(self.driver)
        # launch_calculator(self.driver)
        # sleep(5)  # wait for app to open
        # self.driver.find_element("id", "com.google.android.calculator:id/digit_2").click()
        # self.driver.find_element("id", "com.google.android.calculator:id/op_add").click()
        # self.driver.find_element("id", "com.google.android.calculator:id/digit_3").click()
        # self.driver.find_element("id", "com.google.android.calculator:id/eq").click()
        #
        # # Get result
        # sleep(3)
        # result = self.driver.find_element("id", "com.google.android.calculator:id/history_result").text
        # assert result == "5"
        # hello_world = hw()
        # print(hello_world)
        # assert hello_world == "Hello World"
        # self.driver.terminate_app("com.google.android.calculator")
        # self.driver.lock()
