from abc import abstractmethod, ABC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dataclasses import dataclass
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy

from tools.helper_tools import retry_on_except
brand_path = "/html/body/div[1]/div/div/div/main/div[1]/article/article/fieldset/form/section[1]/div[1]/div/div[1]/div/div/input"
model_path = "/html/body/div[1]/div/div/div/main/div[1]/article/article/fieldset/form/section[1]/div[2]/div/div[1]/div/div/input"
model_popup_button = "/html/body/div[1]/div/div/div/main/div[1]/article/article/fieldset/form/section[1]/div[2]/div/div/div/div/div/div/button/svg"
year_path = "/html/body/div[1]/div/div/div/main/div[1]/article/article/fieldset/form/section[1]/div[4]/div/div[1]/div/div/input"
submit_path = "/html/body/div[1]/div/div/div/main/div[1]/article/article/fieldset/form/section[2]/button[1]"

ignored_exceptions = (NoSuchElementException,StaleElementReferenceException,)

@dataclass
class CarObj:
    name: str = ""
    price: str = ""
    mileage: str = ""
    year: str = ""

class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def click(self, by, path):
        WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions).until(
            EC.visibility_of_element_located((by, path))).click()

    def send_keys(self, by, path, keys):
        element = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions).until(
            EC.visibility_of_element_located((by, path))
        )
        element.clear()
        element.send_keys(keys)

    def get_element(self, by, path):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((by, path))
        )
        return element


class MainPageBase(BaseDriver, ABC):

    @abstractmethod
    def set_brand(self, brand): pass

    @abstractmethod
    def set_model(self, model): pass

    @abstractmethod
    def set_year(self, year): pass

    @abstractmethod
    def get_cars(self, car): pass


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        if driver.platform == "web":
            self.main_page = MainWebPage(driver)
        else:
            self.main_page = MainAndroidPage(driver)

    def get_cars(self, car):
        return self.main_page.get_cars(car)


class MainWebPage(MainPageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.accept_cookies()

    def accept_cookies(self):
        self.click(By.ID, "onetrust-accept-btn-handler")

    @retry_on_except()
    def set_brand(self, car_brand):
        self.click(By.XPATH, brand_path)
        self.send_keys(By.XPATH, brand_path, car_brand)
        self.click(By.ID, car_brand.lower())

    @retry_on_except()
    def set_model(self, car_model):
        self.click(By.XPATH, model_path)
        self.send_keys(By.XPATH, model_path, car_model)
        self.click(By.ID, car_model.lower())

    @retry_on_except()
    def set_year(self, car_year):
        self.click(By.XPATH, year_path)
        self.send_keys(By.XPATH, year_path, car_year)
        self.click(By.ID, car_year)

    @staticmethod
    def parse_car(car_element):
        car_obj = CarObj()
        car_obj.name = car_element.find_element(By.CSS_SELECTOR, "h2").text
        car_obj.price = car_element.find_element(By.CSS_SELECTOR, "h3").text
        car_obj.mileage = car_element.find_element(By.CSS_SELECTOR, '[data-parameter="mileage"]').text
        car_obj.year = car_element.find_element(By.CSS_SELECTOR, '[data-parameter="year"]').text
        return car_obj

    def get_cars(self, car):
        cars = []
        self.set_brand(car.brand)
        self.set_model(car.model)
        self.set_year(car.year)
        self.click(By.XPATH, submit_path)
        results = self.get_element(By.CSS_SELECTOR, '[data-testid="search-results"]')
        car_elements = results.find_elements(By.CSS_SELECTOR, 'article[data-id]')
        for car in car_elements:
            cars.append(self.parse_car(car))
        return cars


class MainAndroidPage(MainPageBase):
    def __init__(self, driver):
        super().__init__(driver)

    def set_brand(self, brand):
        self.click(AppiumBy.XPATH, "//*[contains(@hint, 'Marka')]")
        self.click(AppiumBy.XPATH, "//*[contains(@hint, 'Marka')]")
        self.send_keys(AppiumBy.XPATH, "//*[contains(@hint, 'Marka')]", brand)
        self.click(AppiumBy.ACCESSIBILITY_ID, brand)

    def set_model(self, model):
        self.click(AppiumBy.XPATH, "//*[contains(@hint, 'Wpisz model')]")
        self.send_keys(AppiumBy.XPATH, "//*[contains(@hint, 'Wpisz model')]", model)
        self.click(AppiumBy.ACCESSIBILITY_ID, model)
        self.click(AppiumBy.ACCESSIBILITY_ID, "Pokaż wyniki")

    def set_year(self, year):
        self.click(AppiumBy.XPATH, "//*[contains(@hint, 'Rok produkcji')]")
        self.click(AppiumBy.XPATH, "//*[contains(@hint, 'Od')]")
        self.send_keys(AppiumBy.XPATH, "//*[contains(@hint, 'Od')]", year)
        self.click(AppiumBy.ACCESSIBILITY_ID, "Pokaż wyniki")

    @staticmethod
    def parse_car(car_element):
        car_obj = CarObj()
        car_attrs = car_element.get_attribute("content-desc")
        car_attrs = car_attrs.replace("·", "")
        car_attrs = car_attrs.split("\n")
        if car_attrs[0] == "Wyróżnione":
            car_attrs.pop(0)
        if len(car_attrs) >= 5:
            car_obj.name = car_attrs[2].strip()
            car_obj.price = car_attrs[0].strip()
            car_obj.mileage = car_attrs[4].strip()
            car_obj.year = car_attrs[3].strip()

        return car_obj

    def get_cars(self, car):
        cars = []
        self.set_brand(car.brand)
        self.set_model(car.model)
        self.set_year(car.year)
        self.click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Wyświetl")')
        time.sleep(2)
        scroll_view_element = self.driver.find_element(AppiumBy.CLASS_NAME, "android.widget.ScrollView")

        car_elements = scroll_view_element.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.ImageView").clickable(true)'
        )
        for car in car_elements:
            cars.append(self.parse_car(car))
        return cars
