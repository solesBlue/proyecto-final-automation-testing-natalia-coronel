
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    # 1. LOCATORS
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    _ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")

    # 2. CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Verificar que estamos en la pagina del carrito
        self.wait.until(EC.url_contains("cart.html"))

    # 3. METODOS DE CONSULTA
    def obtener_productos_en_carrito(self):
        """Obtiene la lista de productos en el carrito."""
        return self.driver.find_elements(*self._CART_ITEMS)

    def obtener_nombres_productos(self):
        """Obtiene los nombres de todos los productos en el carrito."""
        elementos_nombre = self.driver.find_elements(*self._ITEM_NAMES)
        return [elemento.text for elemento in elementos_nombre]

    def obtener_precios_productos(self):
        """Obtiene los precios de todos los productos del carrito."""
        elementos_precio = self.driver.find_elements(*self._ITEM_PRICES)
        return [elemento.text for elemento in elementos_precio]

    # 4. METODOS DE ACCION
    def continuar_comprando(self):
        """Regresa a la pagina de inventario."""
        self.driver.find_element(*self._CONTINUE_SHOPPING).click()

        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)

    # def proceder_checkout(self):
    #     """Inicia el proceso de checkout."""
    #     self.driver.find_element(*self._CHECKOUT_BUTTON).click()
    #     return self


    def proceder_checkout(self):
        """Inicia el proceso de checkout."""

        boton_checkout = self.wait.until(
            EC.element_to_be_clickable(self._CHECKOUT_BUTTON)
        )

        boton_checkout.click()

        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    #Se crea un objeto CartPage después de navegar al carrito.
    def ir_al_carrito(self):
        """Navega a la pagina del carrito."""
        self.driver.find_element(*self._CART_LINK).click()

        from pages.cart_page import CartPage
        return CartPage(self.driver)