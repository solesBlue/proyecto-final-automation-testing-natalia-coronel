from selenium.webdriver.common.by import By
from utils.helpers import login
from pages.inventory_page import InventoryPage


## Navegación y verificación del catálogo: (Clases 6 a 8)
# def test_inventario_catalogo(driver):
#     login(driver)  ##utiliza la función login() definida en helpers.py para iniciar sesión antes de realizar las verificaciones del catálogo
    
#     page_title = driver.title
#     section_title = driver.find_element(By.CLASS_NAME, "title").text

#     assert page_title == "Swag Labs", "Error! El título de la página no coincide con 'Swag Labs'. Se indica en el título actual: " + page_title

#     assert section_title == "Products", "Error! El título de la sección no coincide con 'Products'. Se indica en el título actual: " + section_title


def test_inventario_catalogo(driver):
    # Iniciar sesion
    login(driver)

    pagina_inventario = InventoryPage(driver)

    # Obtener los titulos mediante POM
    page_title = pagina_inventario.obtener_titulo_navegador()
    section_title = pagina_inventario.obtener_titulo()

    assert page_title == "Swag Labs", \
        "Error: El título de la página no coincide con 'Swag Labs'. Se indica en el título actual: " + page_title

    assert section_title == "Products", \
        "Error: El título de la sección no coincide con 'Products'. Se indica en el título actual: " + section_title



# def test_inventario_productos_visibles(driver):
#     login(driver)  
#     productos_lista = driver.find_elements(By.CLASS_NAME, "inventory_item")

#     assert len(productos_lista) > 0, "Error! No se encontraron productos visibles en el catálogo."

#     nombre_producto = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
#     precio_producto= driver.find_elements(By.CLASS_NAME, "inventory_item_price")

#     ##requisito: validar que el primer producto tenga nombre y precio
#     nombre_primer_producto = nombre_producto[0].text
#     precio_primer_producto = precio_producto[0].text

#     assert nombre_primer_producto != "", \
#         "Error! El primer producto no posee nombre."

#     assert precio_primer_producto != "", \
#         "Error! El primer producto no posee precio."

#     print("Nombre del producto:", nombre_primer_producto)
#     print("Precio:", precio_primer_producto)

#Aplicando POM (Page Object Model) para el test de productos visibles
def test_inventario_productos_visibles(driver):
    login(driver)
    pagina_inventario = InventoryPage(driver)

    # Obtener los productos mediante POM
    productos_lista = pagina_inventario.obtener_productos()

    assert len(productos_lista) > 0, \
        "Error! No se encontraron productos en el catálogo."

    nombres = pagina_inventario.obtener_nombres_productos()
    precios = pagina_inventario.obtener_precios_productos()

    # Valido que todos los productos tengan nombre y precio
    assert len(nombres) == len(productos_lista), \
        "Error! La cantidad de nombres no coincide con la cantidad de productos."

    assert len(precios) == len(productos_lista), \
        "Error! La cantidad de precios no coincide con la cantidad de productos."

    for i in range(len(productos_lista)):
        nombre = nombres[i].text
        precio = precios[i].text

        assert nombre != "", \
            f"Error! El producto {i + 1} no posee nombre."

        assert precio != "", \
            f"Error! El producto {i + 1} no posee precio."

        print("Producto:", i + 1)
        print("Nombre:", nombre)
        print("Precio:", precio)


# def test_inventario_validar_UI (driver):
#     login(driver)  

#     menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
#     assert menu_button.is_displayed(), "Error! El botón de menú no es visible."

#     filtros = driver.find_element(By.CLASS_NAME, "product_sort_container")
#     assert filtros.is_displayed(), "Error! El filtro de productos no es visible."

#Aplico POM (Page Object Model) para el test de validación de UI
def test_inventario_validar_UI(driver):
    login(driver)

    pagina_inventario = InventoryPage(driver)

    # Validar que el boton de menu  y filtro de producto sean visible
    assert pagina_inventario.esta_menu_visible(), \
        "Error: El botón de menú no esta visible."

    assert pagina_inventario.esta_filtro_visible(), \
        "Error: El filtro de productos no es visible."


# def test_inventario_ordenar_precio(driver):
#     login(driver)  

#     filtros = driver.find_element(
#         By.CLASS_NAME, "product_sort_container" 
#     )

#     filtros.find_element(
#         By.CSS_SELECTOR, "option[value='lohi']"
#     ).click()

#     elementos_precios = driver.find_elements (
#         By.CLASS_NAME, "inventory_item_price"
#     )

#     precios =[]

#     for elemento in elementos_precios:
#         precio = elemento.text.replace("$", "")
#         precios.append(float(precio))

#     assert len(precios) > 0, \
#         "Error: No se encontraron precios de productos."

#     for i in range(len(precios) - 1):
#         assert precios[i] <= precios[i + 1], \
#             f"Error: Los precios no están ordenados correctamente. Precio {precios[i]} es mayor que {precios[i + 1]}."

#Aplico POM (Page Object Model) para el test de ordenamiento de precios
def test_inventario_ordenar_precio(driver):
    login(driver)

    pagina_inventario = InventoryPage(driver)

    # Ordenar productos por precio de menor a mayor
    pagina_inventario.ordenar_precio_ascendente()

    # Obtener los precios de los productos
    elementos_precios = pagina_inventario.obtener_precios_productos()

    precios = []

    for elemento in elementos_precios:
        precio = elemento.text.replace("$", "")
        precios.append(float(precio))

    assert len(precios) > 0, \
        "Error: No se encontraron precios de productos."
    
    # Verificar el ordenamiento de todos los productos
    for i in range(len(precios) - 1):
        assert precios[i] <= precios[i + 1], \
            f"Error: Los precios no están ordenados correctamente. Precio {precios[i]} es mayor que {precios[i + 1]}."