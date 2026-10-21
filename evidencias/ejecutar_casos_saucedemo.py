import json, sys, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
URL = "https://www.saucedemo.com/"
results = {}


def shot(page, name):
    page.screenshot(path=str(OUT / f"{name}.png"), full_page=True)


def login(page, user, pwd="secret_sauce"):
    page.goto(URL)
    page.fill("#user-name", user)
    page.fill("#password", pwd)
    page.click("#login-button")


def record(tc, ok, observado):
    results[tc] = {"estado": "Passed" if ok else "Failed", "observado": observado,
                   "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}


with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = lambda: browser.new_context(viewport={"width": 1280, "height": 800})

    # TC-01 login valido
    page = ctx().new_page()
    login(page, "standard_user")
    title = page.text_content(".title")
    shot(page, "TC-01_login_exitoso")
    record("TC-01", page.url.endswith("/inventory.html") and title == "Products",
           f"URL {page.url}, titulo '{title}'")

    # TC-02 usuario bloqueado
    page = ctx().new_page()
    login(page, "locked_out_user")
    err = page.text_content("[data-test='error']")
    shot(page, "TC-02_usuario_bloqueado")
    record("TC-02", "locked out" in err and page.url == URL, f"Mensaje: '{err}'")

    # TC-03 agregar dos productos y eliminar uno desde el carrito
    page = ctx().new_page()
    login(page, "standard_user")
    page.click("#add-to-cart-sauce-labs-backpack")
    page.click("#add-to-cart-sauce-labs-bike-light")
    badge_antes = page.text_content(".shopping_cart_badge")
    shot(page, "TC-03a_dos_productos_agregados")
    page.click(".shopping_cart_link")
    page.click("#remove-sauce-labs-bike-light")
    items = page.locator(".inventory_item_name").all_text_contents()
    badge_despues = page.text_content(".shopping_cart_badge")
    shot(page, "TC-03b_producto_eliminado")
    record("TC-03", badge_antes == "2" and badge_despues == "1" and items == ["Sauce Labs Backpack"],
           f"Badge {badge_antes} -> {badge_despues}; carrito: {items}")

    # TC-04 checkout con campos obligatorios vacios
    page = ctx().new_page()
    login(page, "standard_user")
    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")
    page.click("#checkout")
    page.click("#continue")
    e1 = page.text_content("[data-test='error']")
    shot(page, "TC-04a_sin_first_name")
    page.fill("#first-name", "Ana")
    page.click("#continue")
    e2 = page.text_content("[data-test='error']")
    page.fill("#last-name", "Quispe")
    page.click("#continue")
    e3 = page.text_content("[data-test='error']")
    shot(page, "TC-04b_sin_postal_code")
    record("TC-04", "First Name is required" in e1 and "Last Name is required" in e2
           and "Postal Code is required" in e3 and "checkout-step-one" in page.url,
           f"Mensajes: '{e1}' | '{e2}' | '{e3}'")

    # TC-05 checkout con carrito vacio
    page = ctx().new_page()
    login(page, "standard_user")
    page.click(".shopping_cart_link")
    vacio = page.locator(".cart_item").count()
    shot(page, "TC-05a_carrito_vacio")
    page.click("#checkout")
    paso1 = page.url
    page.fill("#first-name", "Ana")
    page.fill("#last-name", "Quispe")
    page.fill("#postal-code", "0000")
    page.click("#continue")
    total = page.text_content(".summary_total_label")
    shot(page, "TC-05b_resumen_sin_productos")
    page.click("#finish")
    header = page.text_content(".complete-header")
    shot(page, "TC-05c_orden_completada_vacia")
    bloqueado = "checkout-step-one" not in paso1
    record("TC-05", bloqueado,
           f"Items en carrito: {vacio}; checkout permitido ({paso1}); {total}; mensaje final: '{header}'")

    browser.close()

(OUT / "resultados.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf8")
print(json.dumps(results, indent=2, ensure_ascii=False))
