from tools.main_page import MainPage
from tools.car import Car


class TestLoginPage:
    def test_that_import_working(self, driver):
        volvo_car = Car("Subaru", "Legacy", "2015")
        main_page = MainPage(driver)
        cars = main_page.get_cars(volvo_car)

        for car in cars:
            print("###############################")
            print(car)
            print("###############################")
        assert 1 + 1 == 2
