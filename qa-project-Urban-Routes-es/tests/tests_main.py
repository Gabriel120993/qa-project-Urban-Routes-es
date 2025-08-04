import time
import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.urban_routes_page import UrbanRoutesPage
from helpers.retrieve_phone_code import retrieve_phone_code
import data

@pytest.fixture(scope="class")
def driver_setup(request):
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=capabilities)
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("driver_setup")
class TestUrbanRoutes:

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.page = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        self.page.set_route(data.address_from, data.address_to)
        assert data.address_from in self.driver.page_source

    def test_select_tariff(self):
        self.page.select_comfort_tariff()
        # Asumimos que se refleja algo en la UI
        assert "Comfort" in self.driver.page_source

    def test_enter_phone(self):
        self.page.enter_phone_number(data.phone_number)
        assert data.phone_number in self.driver.page_source

    def test_add_card_and_code(self):
        self.page.enter_card_code(data.card_code)
        code = retrieve_phone_code(self.driver)
        assert len(code) == 4

    def test_submit_card(self):
        self.page.submit_card()
        assert "Tarjeta agregada" in self.driver.page_source

    def test_driver_message(self):
        self.page.add_message_to_driver(data.message)
        assert data.message in self.driver.page_source

    def test_blanket_and_tissues(self):
        self.page.request_blanket_and_tissues()
        # Comprobar algo del DOM que indique que fueron seleccionados

    def test_add_icecreams(self):
        self.page.add_icecreams()
        # Confirmar que aumentó el contador

    def test_confirm_order(self):
        self.page.confirm_order()
        assert "Buscando un taxi" in self.driver.page_source
