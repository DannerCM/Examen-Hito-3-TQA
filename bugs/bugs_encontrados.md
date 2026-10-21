# Bugs encontrados — SauceDemo

| ID | Título | Caso | Severidad | Prioridad | Estado |
|----|--------|------|-----------|-----------|--------|
| BUG-01 | El sistema permite completar una compra con el carrito vacío | TC-05 | Alta (2/5) | Alta (2/5) | Abierto |

---

## BUG-01 — El sistema permite completar una compra con el carrito vacío

| Campo | Detalle |
|-------|---------|
| **ID** | BUG-01 |
| **Título** | El sistema permite completar una compra con el carrito vacío |
| **Descripción** | En https://www.saucedemo.com/ el botón Checkout del carrito está habilitado aunque no haya productos. El flujo llega al resumen con total $0.00 y confirma la orden con "Thank you for your order!". |
| **Referencia** | TC-05 |
| **Precondiciones** | Sesión iniciada con `standard_user` / `secret_sauce`; carrito vacío |
| **Datos** | First Name `Ana`, Last Name `Quispe`, Postal Code `0000` |
| **Ambiente** | Windows 10 Pro, Chromium 156.0.8078.4, versión pública de SauceDemo al 2026-10-20 |
| **Severidad** | Alta — 2 (escala 1-5, 1 = crítica) |
| **Prioridad** | Alta — 2 (escala 1-5, 1 = más urgente) |
| **Estado** | Abierto |

**Pasos para reproducir**

1. Ingresar a https://www.saucedemo.com/.
2. Iniciar sesión con `standard_user` y `secret_sauce`.
3. Sin agregar productos, presionar el ícono del carrito.
4. Presionar Checkout.
5. Completar First Name `Ana`, Last Name `Quispe`, Postal Code `0000` y presionar Continue.
6. Presionar Finish.

**Resultado actual**

El paso 4 abre "Checkout: Your Information". El paso 5 muestra "Checkout: Overview" sin productos, con "Item total: $0" y "Total: $0.00". El paso 6 muestra "Thank you for your order!" y "Your order has been dispatched".

**Resultado esperado**

El botón Checkout debería estar deshabilitado con el carrito vacío, o el sistema debería mostrar un aviso del tipo "Agregue al menos un producto" sin pasar al formulario. En ningún caso debería confirmarse una orden sin productos.

**Evidencia**

- `evidencias/capturas/TC-05a_carrito_vacio.png` — carrito sin productos y botón Checkout habilitado
- `evidencias/capturas/TC-05b_resumen_sin_productos.png` — resumen con total $0.00
- `evidencias/capturas/TC-05c_orden_completada_vacia.png` — confirmación de la orden vacía

**Comentarios (impacto)**

Una tienda real registraría órdenes vacías: el área de despacho las procesaría, se enviarían correos de confirmación sin sentido y las métricas de ventas quedarían contaminadas. No bloquea la compra normal, por eso no es crítica, pero afecta el proceso principal del negocio.

**Reproducibilidad:** 3 de 3 ejecuciones del script `evidencias/ejecutar_casos_saucedemo.py`.
