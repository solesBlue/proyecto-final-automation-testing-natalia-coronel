from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, agregar_primer_producto

def test_checkout_compra_exitosa(driver):
    login(driver)  
    agregar_primer_producto(driver)

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait = WebDriverWait(driver, 10)

    boton_checkout = wait.until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )

    boton_checkout.click()

    campo_nombre = wait.until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )
    campo_nombre.send_keys("Natalia")
    driver.find_element(By.ID, "last-name").send_keys("Coronel")
    driver.find_element(By.ID, "postal-code").send_keys("1708")

    driver.find_element(By.ID, "continue").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/checkout-step-two.html"))

    assert "checkout-step-two.html" in driver.current_url, \
        "Error: No se accedió al resumen de compra."

    driver.find_element(By.ID, "finish").click()

    mensaje = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )

    assert mensaje.text == "Thank you for your order!", \
        "Error: No se visualiza el mensaje de confirmacion de compra."


def test_checkout_campos_obligatorios(driver):
    login(driver)  
    agregar_primer_producto(driver)

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    wait = WebDriverWait(driver, 10)

    boton_checkout = wait.until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )

    # boton_checkout.click()
    # driver.find_element(By.ID, "continue").click()

    boton_checkout.click()

    # Esperar a que se visualice el formulario de checkout
    boton_continuar = wait.until(
        EC.element_to_be_clickable((By.ID, "continue"))
    )

    # Intenta continuar sin completar los campos
    boton_continuar.click()

    wait = WebDriverWait(driver, 10)
    mensaje_error = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )

    assert mensaje_error.text == "Error: First Name is required", \
        "Error: Complete el campo Nombre."

    assert "checkout-step-two.html" not in driver.current_url, \
        "Error: El checkout avanzo sin completar los campos obligatorios."