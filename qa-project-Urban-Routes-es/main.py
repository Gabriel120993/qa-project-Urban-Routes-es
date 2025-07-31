from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import data

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_route(self, from_address, to_address):
            self.driver.find_element(*self.from_field).send_keys(from_address)
            self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

        # Tarifa
    def select_comfort_tariff(self):
        self.driver.find_element(By.ID, "tariff-comfort").click()

        # Teléfono
    def enter_phone_number(self, number):
        self.driver.find_element(By.ID, "phone").send_keys(number)
        self.driver.find_element(By.ID, "send-phone").click()

    def enter_phone_code(self, code):
        self.driver.find_element(By.ID, "code").send_keys(code)
        self.driver.find_element(By.ID, "confirm-phone").click()

        # Tarjeta
    def add_credit_card(self, number, expiry, cvv):
        self.driver.find_element(By.ID, "add-card").click()
        self.driver.find_element(By.ID, "card-number").send_keys(number)
        self.driver.find_element(By.ID, "expiry").send_keys(expiry)
        cvv_input = self.driver.find_element(By.CLASS_NAME, "card-input")
        cvv_input.send_keys(cvv)
        cvv_input.send_keys(Keys.TAB)  # activar botón "link"
        self.driver.find_element(By.ID, "link").click()

        # Mensaje al conductor
    def write_driver_message(self, message):
            self.driver.find_element(By.ID, "comment").send_keys(message)

       # Servicios extra
    def request_blanket_and_tissues(self):
        self.driver.find_element(By.ID, "blanket").click()
        self.driver.find_element(By.ID, "tissues").click()

    def request_ice_cream(self, quantity):
        for _ in range(quantity):
            self.driver.find_element(By.ID, "ice-cream").click()

        # Solicitar taxi
    def request_taxi(self):
            self.driver.find_element(By.ID, "request-taxi").click()

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "driver-info"))
        )

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_full_ride_flow(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)

        # Paso 1: ingresar direcciones
        page.set_route(data.address_from, data.address_to)
        assert page.get_from() == data.address_from
        assert page.get_to() == data.address_to

        # Paso 2: seleccionar tarifa Comfort
        page.select_comfort_tariff()

        # Paso 3: ingresar teléfono y confirmar
        phone = "+1 123 123 12 12"
        page.enter_phone_number(phone)
        time.sleep(2)
        code = retrieve_phone_code(self.driver)
        page.enter_phone_code(code)

        # Paso 4: agregar tarjeta
        page.add_credit_card("1234 5678 9100', '111")

        # Paso 5: mensaje para conductor
        page.write_driver_message("Muéstrame el camino al museo")

        # Paso 6: pedir manta y pañuelos
        page.request_blanket_and_tissues()

        # Paso 7: pedir dos helados
        page.request_ice_cream(2)

        # Paso 8: solicitar taxi
        page.request_taxi()

        # Paso 9: esperar información del conductor
        page.wait_for_driver_info()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
