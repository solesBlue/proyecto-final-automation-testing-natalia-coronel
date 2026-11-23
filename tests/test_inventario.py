from selenium.webdriver.common.by import By
from utils.helpers import login

## Navegación y verificación del catálogo: (Clases 6 a 8)
def test_inventario_catalogo(driver):
    login(driver)  ##utiliza la función login() definida en helpers.py para iniciar sesión antes de realizar las verificaciones del catálogo
    
    page_title = driver.title
    section_title = driver.find_element(By.CLASS_NAME, "title").text

    assert page_title == "Swag Labs", "Error! El título de la página no coincide con 'Swag Labs'. Se indica en el título actual: " + page_title

    assert section_title == "Products", "Error! El título de la sección no coincide con 'Products'. Se indica en el título actual: " + section_title

def test_inventario_productos_visibles(driver):
    login(driver)  
    productos_lista = driver.find_elements(By.CLASS_NAME, "inventory_item")

    assert len(productos_lista) > 0, "Error! No se encontraron productos visibles en el catálogo."

    nombre_producto = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    precio_producto= driver.find_elements(By.CLASS_NAME, "inventory_item_price")

    ##requisito: validar que el primer producto tenga nombre y precio
    nombre_primer_producto = nombre_producto[0].text
    precio_primer_producto = precio_producto[0].text

    assert nombre_primer_producto != "", \
        "Error! El primer producto no posee nombre."

    assert precio_primer_producto != "", \
        "Error! El primer producto no posee precio."

    print("Nombre del producto:", nombre_primer_producto)
    print("Precio:", precio_primer_producto)


def test_inventario_validar_UI (driver):
    login(driver)  

    menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
    assert menu_button.is_displayed(), "Error! El botón de menú no es visible."

    filtros = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert filtros.is_displayed(), "Error! El filtro de productos no es visible."


def test_inventario_ordenar_precio(driver):
    login(driver)  

    filtros = driver.find_element(
        By.CLASS_NAME, "product_sort_container" 
    )

    filtros.find_element(
        By.CSS_SELECTOR, "option[value='lohi']"
    ).click()

    elementos_precios = driver.find_elements (
        By.CLASS_NAME, "inventory_item_price"
    )

    precios =[]

    for elemento in elementos_precios:
        precio = elemento.text.replace("$", "")
        precios.append(float(precio))

    assert len(precios) > 0, \
        "Error: No se encontraron precios de productos."

    for i in range(len(precios) - 1):
        assert precios[i] <= precios[i + 1], \
            f"Error: Los precios no están ordenados correctamente. Precio {precios[i]} es mayor que {precios[i + 1]}."