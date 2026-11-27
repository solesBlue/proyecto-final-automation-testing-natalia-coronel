
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:

    # 1. LOCATORS
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _FINISH_BUTTON = (By.ID, "finish")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    # 2. CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 3. METODOS DE ACCION
    def completar_datos(self, nombre: str, apellido: str, codigo_postal: str):
        """Completa los datos del comprador."""

        campo_nombre = self.wait.until(
            EC.visibility_of_element_located(self._FIRST_NAME)
        )

        campo_nombre.clear()
        campo_nombre.send_keys(nombre)

        campo_apellido = self.driver.find_element(*self._LAST_NAME)
        campo_apellido.clear()
        campo_apellido.send_keys(apellido)

        campo_codigo = self.driver.find_element(*self._POSTAL_CODE)
        campo_codigo.clear()
        campo_codigo.send_keys(codigo_postal)

        return self

    def continuar(self):
        """Presiona el boton Continue."""

        boton_continuar = self.wait.until(
            EC.element_to_be_clickable(self._CONTINUE_BUTTON)
        )

        boton_continuar.click()
        return self

    def finalizar_compra(self):
        """Presiona el boton Finish."""

        boton_finalizar = self.wait.until(
            EC.element_to_be_clickable(self._FINISH_BUTTON)
        )

        boton_finalizar.click()
        return self

    # 4. METODOS DE VERIFICACION
    def esta_en_resumen(self) -> bool:
        """Verifica que se accedio al resumen de compra."""

        self.wait.until(
            EC.url_contains("checkout-step-two.html")
        )

        return "checkout-step-two.html" in self.driver.current_url

    def obtener_mensaje_confirmacion(self) -> str:
        """Obtiene el mensaje de compra exitosa."""

        mensaje = self.wait.until(
            EC.visibility_of_element_located(self._COMPLETE_HEADER)
        )

        return mensaje.text

    def obtener_mensaje_error(self) -> str:
        """Obtiene el mensaje de error del checkout."""

        mensaje = self.wait.until(
            EC.visibility_of_element_located(self._ERROR_MESSAGE)
        )

        return mensaje.text

