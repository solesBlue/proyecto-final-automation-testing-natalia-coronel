import pytest
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

with open("data/usuarios.json", "r", encoding="utf-8") as archivo:
    datos_usuarios = json.load(archivo)

## Automatización de Login
def test_login_valido(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.url_contains("/inventory.html")
    )
    assert "/inventory.html" in driver.current_url, "Error! Login failed: No se redirigió a la página de inventario (/inventory.html)."


    inicio_producto = driver.find_element(By.CSS_SELECTOR, ".title")

    assert inicio_producto.text == "Products", \
        "Error! No se visualiza la sección Products."


def test_login_invalido(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()

    # Intentar iniciar sesion con credenciales incorrectas
    pagina_login.login_completo(
        "usuario_invalido",
        "password_invalida"
    )

    mensaje_error = pagina_login.obtener_mensaje_error()

    assert mensaje_error != "", \
        "Error: No se visualiza el mensaje de error al ingresar credenciales invalidas."


@pytest.mark.parametrize("datos", datos_usuarios)
def test_login_parametrizado(driver, datos):
    pagina_login = LoginPage(driver)

    # Abre la pagina e iniciar sesion con datos JSON
    pagina_login.abrir()
    pagina_login.login_completo(
        datos["usuario"],
        datos["clave"]
    )

    if datos["debe_funcionar"]:
        # Valido el acceso al inventario
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("inventory.html"))

        assert "inventory.html" in driver.current_url, \
            "Error: El usuario no pudo iniciar sesion."

    else:
        mensaje_error = pagina_login.obtener_mensaje_error()

        assert mensaje_error != "", \
            "Error: No se muestra un mensaje para el login con error."
