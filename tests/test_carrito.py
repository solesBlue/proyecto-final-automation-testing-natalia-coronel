from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, agregar_primer_producto
from pages.inventory_page import InventoryPage

## Interacción con productos: (Clase 8)
# def test_carrito_agregar_producto(driver):
#     login(driver)  

#     # boton_agregar = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0]
#     # boton_agregar.click()

#     agregar_primer_producto(driver)

#     # Esperar que el botón cambie a "Remove"
#     wait = WebDriverWait(driver, 10)
#     wait.until(
#         EC.text_to_be_present_in_element((By.CLASS_NAME, "btn_inventory"),"Remove")
#     )

#     boton_remove = driver.find_elements(By.CLASS_NAME,"btn_inventory")[0]
#     assert boton_remove.text == "Remove", "Error! El botón no cambió a 'Remove' después de agregar el producto al carrito."

#Aplico POM para el test de agregar producto al carrito
def test_carrito_agregar_producto(driver):
    login(driver)

    pagina_inventario = InventoryPage(driver)

    # Agregar el primer producto al carrito
    pagina_inventario.agregar_primer_producto()

    boton_remove = pagina_inventario.obtener_texto_primer_boton()

    assert boton_remove == "Remove", \
        "Error! El botón no cambió a 'Remove' después de agregar el producto al carrito."


# def test_carrito_verificar_carrito(driver):
#     login(driver)  
#     agregar_primer_producto(driver)

#     wait = WebDriverWait(driver, 10)
#     wait.until(
#         EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"),"1")
#     )

#     contador_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
#     assert contador_carrito == "1", "Error! El contador del carrito no muestra '1' después de agregar un producto. Se muestra: " + contador_carrito

#Agregro POM para el test de verificar el carrito

def test_carrito_verificar_carrito(driver):
    login(driver)

    pagina_inventario = InventoryPage(driver)

    pagina_inventario.agregar_primer_producto()

    contador_carrito = pagina_inventario.obtener_contador_carrito()

    assert contador_carrito == 1, \
        f"Error: El contador del carrito no muestra 1 después de agregar un producto. Se muestra: {contador_carrito}"


# def test_carrito_navegar_carrito(driver):
#     login(driver)  

#     driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.url_contains("/cart.html"))

#     assert "/cart.html" in driver.current_url, "Error: No se redirigió a la página del carrito (/cart.html)."

#Aplico POM para el test de navegar al carrito
def test_carrito_navegar_carrito(driver):
    login(driver)

    pagina_inventario = InventoryPage(driver)

    # Navegar al carrito mediante POM
    pagina_carrito = pagina_inventario.ir_al_carrito()

    assert "/cart.html" in pagina_carrito.driver.current_url, \
        "Error! No se redirigió a la página del carrito (/cart.html)."


# def test_carrito_verificar_producto_agregado(driver):
#     login(driver)  

#     # Obtener datos del primer producto
#     nombre_producto = driver.find_elements(By.CLASS_NAME,"inventory_item_name")[0].text
#     precio_producto = driver.find_elements(By.CLASS_NAME,"inventory_item_price")[0].text

#     agregar_primer_producto(driver)
#     driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.url_contains("/cart.html")
# )

#     nombre_producto_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
#     precio_producto_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

#     assert nombre_producto_carrito == nombre_producto, \
#         "Error! El producto del carrito no coincide con el producto agregado."

#     assert precio_producto_carrito == precio_producto, \
#         "Error! El precio del producto en el carrito no coincide con el precio del catálogo."

#     print("Nombre del producto en el carrito:", nombre_producto_carrito)
#     print("Precio del producto en el carrito:", precio_producto_carrito)


def test_carrito_verificar_producto_agregado(driver):
    login(driver)

    pagina_inventario = InventoryPage(driver)

    # Obtener los datos del primer producto
    nombres = pagina_inventario.obtener_nombres_productos()
    precios = pagina_inventario.obtener_precios_productos()

    nombre_producto = nombres[0].text
    precio_producto = precios[0].text

    # Agregar el producto al carrito
    pagina_inventario.agregar_primer_producto()

    # Navegar al carrito mediante POM
    pagina_carrito = pagina_inventario.ir_al_carrito()

    productos_carrito = pagina_carrito.obtener_productos_en_carrito()

    # Validar la cantidad de productos
    assert len(productos_carrito) == 1, \
        "Error! El carrito no contiene exactamente un producto."

    nombres_carrito = pagina_carrito.obtener_nombres_productos()
    precios_carrito = pagina_carrito.obtener_precios_productos()

    nombre_producto_carrito = nombres_carrito[0]
    precio_producto_carrito = precios_carrito[0]

    assert nombre_producto_carrito == nombre_producto, \
        "Error! El producto del carrito no coincide con el producto agregado."

    assert precio_producto_carrito == precio_producto, \
        "Error! El precio del producto en el carrito no coincide con el precio del catálogo."

    print("Nombre del producto en el carrito:", nombre_producto_carrito)
    print("Precio del producto en el carrito:", precio_producto_carrito)
