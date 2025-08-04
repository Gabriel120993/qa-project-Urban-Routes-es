from selenium.webdriver.common.by import By

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff = (By.CLASS_NAME, 'tariff_comfort')
    phone_input = (By.ID, 'phone')
    code_input = (By.ID, 'code')
    submit_button = (By.ID, 'submit')
    message_input = (By.ID, 'comment')
    blanket_checkbox = (By.ID, 'blanket')
    tissue_checkbox = (By.ID, 'tissues')
    icecream_plus = (By.ID, 'icecream')
    order_button = (By.ID, 'order')

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.from_field).send_keys(address_from)
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def enter_phone_number(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)

    def enter_card_code(self, code):
        card_input = self.driver.find_element(*self.code_input)
        card_input.send_keys(code)
        card_input.send_keys("\t")  # Simula TAB para activar el botón

    def submit_card(self):
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
