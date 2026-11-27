from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_inventario_catalogo(driver):
    # Iniciar sesion
    #login(driver)
    #al implementar POM dejo de usar la función login() y utilizo las clases LoginPage e InventoryPage
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    # Espera a que se cargue el inventario
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory.html"))

    pagina_inventario = InventoryPage(driver)

    # Obtener los titulos mediante POM
    page_title = pagina_inventario.obtener_titulo_navegador()
    section_title = pagina_inventario.obtener_titulo()

    assert page_title == "Swag Labs", \
        "Error: El título de la página no coincide con 'Swag Labs'. Se indica en el título actual: " + page_title

    assert section_title == "Products", \
        "Error: El título de la sección no coincide con 'Products'. Se indica en el título actual: " + section_title


#Aplicando POM (Page Object Model) para el test de productos visibles
def test_inventario_productos_visibles(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    pagina_inventario = InventoryPage(driver)

    # Obtengo los productos mediante POM
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


#Aplico POM (Page Object Model) para el test de validación de UI
def test_inventario_validar_UI(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

    pagina_inventario = InventoryPage(driver)

    # Valido que el boton de menu  y filtro de producto sean visible
    assert pagina_inventario.esta_menu_visible(), \
        "Error: El botón de menú no esta visible."

    assert pagina_inventario.esta_filtro_visible(), \
        "Error: El filtro de productos no es visible."


#Aplico POM (Page Object Model) para el test de ordenamiento de precios
def test_inventario_ordenar_precio(driver):
    pagina_login = LoginPage(driver)
    pagina_login.abrir()
    pagina_login.login_completo("standard_user", "secret_sauce")

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