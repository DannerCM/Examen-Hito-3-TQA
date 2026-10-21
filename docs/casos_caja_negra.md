# Casos de prueba de caja negra — SauceDemo

**Aplicación:** https://www.saucedemo.com/ (Swag Labs)
**Ambiente:** Windows 10 Pro, Chromium 156.0.8078.4 (Playwright 1.64.0), resolución 1280x800
**Fecha de ejecución:** 2026-10-20
**Contraseña de los usuarios de demostración:** `secret_sauce`

## Resumen de ejecución

| ID | Título | Módulo | Tipo | Prioridad | Estado | Defecto |
|----|--------|--------|------|-----------|--------|---------|
| TC-01 | Inicio de sesión con credenciales válidas | Login | Funcional positiva | Alta | Passed | N/A |
| TC-02 | Inicio de sesión con usuario bloqueado | Login | Funcional negativa | Alta | Passed | N/A |
| TC-03 | Agregar dos productos y eliminar uno desde el carrito | Carrito | Funcional positiva | Alta | Passed | N/A |
| TC-04 | Checkout con campos obligatorios vacíos | Checkout | Funcional negativa | Media | Passed | N/A |
| TC-05 | Checkout con el carrito vacío | Checkout | Funcional negativa | Alta | **Failed** | BUG-01 |

Resultado: 4 Passed, 1 Failed. Los casos se ejecutaron con el script `evidencias/ejecutar_casos_saucedemo.py`, que repite los pasos de cada caso en el navegador y guarda las capturas en `evidencias/capturas/`.

---

## TC-01 — Inicio de sesión con credenciales válidas

| Campo | Valor |
|-------|-------|
| Objetivo | Verificar que un usuario válido accede al catálogo de productos |
| Precondiciones | Navegador abierto en https://www.saucedemo.com/ sin sesión iniciada |
| Datos de prueba | Usuario `standard_user`, contraseña `secret_sauce` |

| # | Paso | Dato | Resultado esperado |
|---|------|------|--------------------|
| 1 | Ingresar el usuario en el campo Username | `standard_user` | El campo muestra el usuario |
| 2 | Ingresar la contraseña en el campo Password | `secret_sauce` | El campo muestra caracteres ocultos |
| 3 | Presionar Login | — | Se carga `/inventory.html` con el título "Products" |

**Resultado esperado final:** el usuario entra al catálogo.
**Resultado obtenido:** se cargó `https://www.saucedemo.com/inventory.html` con el título "Products".
**Estado:** Passed
**Evidencia:** `evidencias/capturas/TC-01_login_exitoso.png`

---

## TC-02 — Inicio de sesión con usuario bloqueado

| Campo | Valor |
|-------|-------|
| Objetivo | Verificar que un usuario bloqueado no puede ingresar y recibe un mensaje claro |
| Precondiciones | Navegador abierto en la página de login sin sesión iniciada |
| Datos de prueba | Usuario `locked_out_user`, contraseña `secret_sauce` |

| # | Paso | Dato | Resultado esperado |
|---|------|------|--------------------|
| 1 | Ingresar el usuario | `locked_out_user` | El campo muestra el usuario |
| 2 | Ingresar la contraseña | `secret_sauce` | El campo muestra caracteres ocultos |
| 3 | Presionar Login | — | Se permanece en el login y aparece un mensaje de usuario bloqueado |

**Resultado esperado final:** el acceso se rechaza con un mensaje de bloqueo.
**Resultado obtenido:** el sistema permaneció en el login y mostró "Epic sadface: Sorry, this user has been locked out."
**Estado:** Passed
**Evidencia:** `evidencias/capturas/TC-02_usuario_bloqueado.png`

---

## TC-03 — Agregar dos productos y eliminar uno desde el carrito

| Campo | Valor |
|-------|-------|
| Objetivo | Verificar que el carrito y su contador se actualizan al agregar y eliminar productos |
| Precondiciones | Sesión iniciada con `standard_user`, carrito vacío |
| Datos de prueba | Productos "Sauce Labs Backpack" y "Sauce Labs Bike Light" |

| # | Paso | Dato | Resultado esperado |
|---|------|------|--------------------|
| 1 | Presionar "Add to cart" en el primer producto | Sauce Labs Backpack | El contador del carrito muestra 1 |
| 2 | Presionar "Add to cart" en el segundo producto | Sauce Labs Bike Light | El contador del carrito muestra 2 |
| 3 | Abrir el carrito | — | Se listan los dos productos |
| 4 | Presionar "Remove" en Sauce Labs Bike Light | — | El producto sale de la lista y el contador muestra 1 |

**Resultado esperado final:** el carrito contiene solo "Sauce Labs Backpack" y el contador indica 1.
**Resultado obtenido:** el contador pasó de 2 a 1 y el carrito quedó con "Sauce Labs Backpack".
**Estado:** Passed
**Evidencia:** `TC-03a_dos_productos_agregados.png`, `TC-03b_producto_eliminado.png`

---

## TC-04 — Checkout con campos obligatorios vacíos

| Campo | Valor |
|-------|-------|
| Objetivo | Verificar que el formulario de checkout exige First Name, Last Name y Postal Code |
| Precondiciones | Sesión iniciada con `standard_user` y "Sauce Labs Backpack" en el carrito |
| Datos de prueba | First Name `Ana`, Last Name `Quispe`, Postal Code vacío |

| # | Paso | Dato | Resultado esperado |
|---|------|------|--------------------|
| 1 | Abrir el carrito y presionar Checkout | — | Se carga "Checkout: Your Information" |
| 2 | Presionar Continue con todos los campos vacíos | — | Mensaje "Error: First Name is required" |
| 3 | Completar First Name y presionar Continue | `Ana` | Mensaje "Error: Last Name is required" |
| 4 | Completar Last Name y presionar Continue | `Quispe` | Mensaje "Error: Postal Code is required" y no se avanza |

**Resultado esperado final:** el sistema no avanza mientras falte un campo obligatorio e indica cuál falta.
**Resultado obtenido:** se mostraron, en orden, los tres mensajes de error y la página siguió en `checkout-step-one`.
**Estado:** Passed
**Evidencia:** `TC-04a_sin_first_name.png`, `TC-04b_sin_postal_code.png`

---

## TC-05 — Checkout con el carrito vacío

| Campo | Valor |
|-------|-------|
| Objetivo | Verificar que no se puede completar una compra sin productos en el carrito |
| Precondiciones | Sesión iniciada con `standard_user`, carrito vacío |
| Datos de prueba | First Name `Ana`, Last Name `Quispe`, Postal Code `0000` |

| # | Paso | Dato | Resultado esperado |
|---|------|------|--------------------|
| 1 | Abrir el carrito sin agregar productos | — | El carrito aparece vacío |
| 2 | Presionar Checkout | — | El botón está deshabilitado o el sistema indica que el carrito está vacío |
| 3 | (Si el sistema permite avanzar) completar el formulario y presionar Continue | Ana / Quispe / 0000 | No debe mostrarse un resumen de compra sin productos |
| 4 | Presionar Finish | — | No debe registrarse ninguna orden |

**Resultado esperado final:** la compra se bloquea porque no hay productos.
**Resultado obtenido:** el sistema permitió avanzar a `checkout-step-one`, mostró un resumen con "Total: $0.00" y al presionar Finish confirmó "Thank you for your order!".
**Estado:** Failed
**Defecto:** BUG-01 (ver `bugs/bugs_encontrados.md`)
**Evidencia:** `TC-05a_carrito_vacio.png`, `TC-05b_resumen_sin_productos.png`, `TC-05c_orden_completada_vacia.png`
