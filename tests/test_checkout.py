import json
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

with open("data/checkout.json", "r", encoding="utf-8") as archivo:
    datos_checkout = json.load(archivo)

@pytest.mark.parametrize("datos", datos_checkout)
def test_checkout_compra_exitosa(driver, datos):
    # Inicio sesion mediante LoginPage
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    # Esperar hasta acceder al inventario
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

    pagina_inventario = InventoryPage(driver)

    pagina_inventario.agregar_primer_producto()
    pagina_carrito = pagina_inventario.ir_al_carrito()

    # Inicia el checkout y completa los datos del comprador
    pagina_checkout = pagina_carrito.proceder_checkout()
    pagina_checkout.completar_datos(
        datos["nombre"],
        datos["apellido"],
        datos["codigo_postal"]
    )

    # Continuo al resumen de compra y valido que se accedió correctamente
    pagina_checkout.continuar()
    assert pagina_checkout.esta_en_resumen(), \
        "Error: No se accedió al resumen de compra."

    # Finalizo la compra y obtiene msj de confirmación
    pagina_checkout.finalizar_compra()
    mensaje = pagina_checkout.obtener_mensaje_confirmacion()

    # Valida que la compra fue exitosa
    assert mensaje == "Thank you for your order!", \
        "Error: No se visualiza el mensaje de confirmacion de compra."


def test_checkout_campos_obligatorios(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

    pagina_inventario = InventoryPage(driver)

    pagina_inventario.agregar_primer_producto()
    pagina_carrito = pagina_inventario.ir_al_carrito()

    # Inicia el checkout e intenta continuar sin completar los campos del comprador
    pagina_checkout = pagina_carrito.proceder_checkout()
    pagina_checkout.continuar()

    # Obtiene el mensaje de error y lo valida
    mensaje_error = pagina_checkout.obtener_mensaje_error()
    assert mensaje_error == "Error: First Name is required", \
        "Error: Complete el campo Nombre."

    # Verifica que no se accedio al resumen de compra
    assert "checkout-step-two.html" not in driver.current_url, \
        "Error: El checkout avanzo sin completar los campos obligatorios."
