
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:

    # 1. LOCATORS
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price") 
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _SORT_FILTER = (By.CLASS_NAME, "product_sort_container")      

    # 2. CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 3. METODOS DE CONSULTA
    def obtener_titulo(self):
        """Obtiene el titulo de la pagina de inventario."""
        return self.driver.find_element(*self._TITLE).text

    def obtener_titulo_navegador(self):
        """Obtiene el titulo de la pestaña del navegador."""
        return self.driver.title

    def obtener_productos(self):
        """Obtiene la lista de productos disponibles."""
        return self.driver.find_elements(*self._PRODUCTS)

    # 4. METODOS DE ACCION
    def agregar_primer_producto(self):
        """Agrega el primer producto disponible al carrito."""
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS)[0]
        primer_boton.click()
        return self

    def obtener_contador_carrito(self):
        """Obtiene el numero de productos en el carrito."""
        try:
            badge = self.driver.find_element(*self._CART_BADGE)
            return int(badge.text)
        except:
            return 0

    def obtener_nombres_productos(self):
        """Obtiene los nombres de los productos."""
        return self.driver.find_elements(*self._PRODUCT_NAMES)

    def obtener_precios_productos(self):
        """Obtiene los precios de los productos."""
        return self.driver.find_elements(*self._PRODUCT_PRICES)

    #clase 9: Indica que esperamos que el método devuelva un valor booleano
    def esta_menu_visible(self) -> bool:
        """Verifica si el boton de menu esta visible."""
        return self.driver.find_element(
            *self._MENU_BUTTON
        ).is_displayed()

    def esta_filtro_visible(self) -> bool:
        """Verifica si el filtro de ordenamiento esta visible."""
        return self.driver.find_element(
            *self._SORT_FILTER
        ).is_displayed()


    def ordenar_precio_ascendente(self):
        """Ordena los productos de menor a mayor precio."""

        filtros = self.wait.until(
            EC.element_to_be_clickable(self._SORT_FILTER)
        )

        filtros.find_element(
            By.CSS_SELECTOR, "option[value='lohi']"
        ).click()

        return self
