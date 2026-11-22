from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, agregar_primer_producto


## Interacción con productos: (Clase 8)
def test_carrito_agregar_producto(driver):
    login(driver)  

    # boton_agregar = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0]
    # boton_agregar.click()

    agregar_primer_producto(driver)

    # Esperar que el botón cambie a "Remove"
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "btn_inventory"),"Remove")
    )

    boton_remove = driver.find_elements(By.CLASS_NAME,"btn_inventory")[0]
    assert boton_remove.text == "Remove", "Error! El botón no cambió a 'Remove' después de agregar el producto al carrito."

def test_carrito_verificar_carrito(driver):
    login(driver)  
    agregar_primer_producto(driver)

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"),"1")
    )

    contador_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert contador_carrito == "1", "Error! El contador del carrito no muestra '1' después de agregar un producto. Se muestra: " + contador_carrito

def test_carrito_navegar_carrito(driver):
    login(driver)  

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/cart.html"))

    assert "/cart.html" in driver.current_url, "Error! No se redirigió a la página del carrito (/cart.html)."

def test_carrito_verificar_producto_agregado(driver):
    login(driver)  

    # Obtener datos del primer producto
    nombre_producto = driver.find_elements(By.CLASS_NAME,"inventory_item_name")[0].text
    precio_producto = driver.find_elements(By.CLASS_NAME,"inventory_item_price")[0].text

    agregar_primer_producto(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/cart.html")
)

    nombre_producto_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio_producto_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

    assert nombre_producto_carrito == nombre_producto, \
        "Error! El producto del carrito no coincide con el producto agregado."

    assert precio_producto_carrito == precio_producto, \
        "Error! El precio del producto en el carrito no coincide con el precio del catálogo."

    print("Nombre del producto en el carrito:", nombre_producto_carrito)
    print("Precio del producto en el carrito:", precio_producto_carrito)
