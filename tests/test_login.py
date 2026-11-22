
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

##Login inválido
def test_login_invalido(driver):
    driver.get("https://www.saucedemo.com/")
    
    driver.find_element(By.ID, "user-name").send_keys("usuario_invalido")
    driver.find_element(By.ID, "password").send_keys("contrasena_invalida")
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 10)
    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='error']")
        )
    )

    error_message = mensaje_error.text
    # assert error_message != "", "Error: Inicio desesión con credenciales inválidas."
    assert error_message != "", "Error: No se visualiza el mensaje de error al ingresar credenciales inválidas."