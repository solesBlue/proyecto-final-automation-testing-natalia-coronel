from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.helpers import login, agregar_primer_producto

def test_checkout_compra_exitosa(driver):
    login(driver)  
    agregar_primer_producto(driver)

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    driver.find_element(By.ID, "checkout").click()

    driver.find_element(By.ID, "first-name").send_keys("Natalia")
    driver.find_element(By.ID, "last-name").send_keys("Coronel")
    driver.find_element(By.ID, "postal-code").send_keys("1708")

    driver.find_element(By.ID, "continue").click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("/checkout-step-two.html"))

    assert "checkout-step-two.html" in driver.current_url, \
        "Error: No se accedió al resumen de compra."

    driver.find_element(By.ID, "finish").click()

    mensaje = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))

    assert mensaje.text == "Thank you for your order!", \
        "Error: No se visualiza el mensaje de confirmacion de compra."