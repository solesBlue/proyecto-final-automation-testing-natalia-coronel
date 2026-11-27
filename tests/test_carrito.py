from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

#Aplico POM para el test de agregar producto al carrito
def test_carrito_agregar_producto(driver):
    #login(driver)
    #Utilizo POM para el login
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

    pagina_inventario = InventoryPage(driver)

    # Agregar el primer producto al carrito
    pagina_inventario.agregar_primer_producto()

    boton_remove = pagina_inventario.obtener_texto_primer_boton()

    assert boton_remove == "Remove", \
        "Error! El botón no cambió a 'Remove' después de agregar el producto al carrito."


#Agregro POM para el test de verificar el carrito
def test_carrito_verificar_carrito(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

    pagina_inventario = InventoryPage(driver)

    pagina_inventario.agregar_primer_producto()

    contador_carrito = pagina_inventario.obtener_contador_carrito()

    assert contador_carrito == 1, \
        f"Error: El contador del carrito no muestra 1 después de agregar un producto. Se muestra: {contador_carrito}"


#Aplico POM para el test de navegar al carrito
def test_carrito_navegar_carrito(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

    pagina_inventario = InventoryPage(driver)

    # Navegar al carrito mediante POM
    pagina_carrito = pagina_inventario.ir_al_carrito()

    assert "/cart.html" in pagina_carrito.driver.current_url, \
        "Error! No se redirigió a la página del carrito (/cart.html)."


def test_carrito_verificar_producto_agregado(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

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
