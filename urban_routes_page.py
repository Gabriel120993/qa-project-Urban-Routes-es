from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        # Localizadores
        self.from_field = (By.ID, "from")
        self.to_field = (By.ID, "to")
        self.comfort_tariff = (By.CLASS_NAME, "tariff_comfort")
        self.phone_input = (By.ID, "phone")
        self.card_number_input = (By.ID, "number")
        self.card_code_input = (By.ID, "code")
        self.card_link_button = (By.ID, "link")
        self.submit_button = (By.ID, "submit")
        self.message_input = (By.ID, "comment")
        self.blanket_checkbox = (By.ID, "blanket")
        self.tissue_checkbox = (By.ID, "tissues")
        self.icecream_plus = (By.ID, "icecream")
        self.order_button = (By.ID, "order")
        self.modal_search = (By.CLASS_NAME, "order-search")  # Ajustar si es distinto
        self.driver_info_modal = (By.CLASS_NAME, "order-assigned")  # Ajustar si es distinto

    # --- Métodos de interacción ---

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.from_field).send_keys(address_from)
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)

    def enter_card_details(self, number, code):
        self.driver.find_element(*self.card_number_input).send_keys(number)
        code_field = self.driver.find_element(*self.card_code_input)
        code_field.send_keys(code)
        code_field.send_keys(Keys.TAB)  # Cambia el foco para activar el botón

    def link_card(self):
        self.driver.find_element(*self.card_link_button).click()

    def submit_phone_code(self, code):
        self.driver.find_element(*self.submit_button).send_keys(code)
        self.driver.find_element(*self.submit_button).click()

    def add_message_to_driver(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_checkbox).click()
        self.driver.find_element(*self.tissue_checkbox).click()

    def add_icecreams(self, count=2):
        for _ in range(count):
            self.driver.find_element(*self.icecream_plus).click()

    def confirm_order(self):
        self.driver.find_element(*self.order_button).click()

    # --- Métodos de espera para modales ---
    def wait_for_search_modal(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.modal_search)
        )

    def wait_for_driver_info(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.driver_info_modal)
        )
