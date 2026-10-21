# Escenarios Gherkin — SauceDemo

Los escenarios describen el comportamiento esperado de dos funcionalidades probadas en los casos de caja negra. Cada escenario se relaciona con su caso de prueba mediante una etiqueta. Gherkin documenta el comportamiento; no ejecuta las pruebas por sí solo.

## Feature 1: Inicio de sesión

```gherkin
Feature: Inicio de sesión en Swag Labs
  Como cliente de la tienda
  Quiero iniciar sesión con mi usuario
  Para acceder al catálogo de productos

  Background:
    Given que estoy en la página de login de "https://www.saucedemo.com/"

  @TC-01 @exitoso
  Scenario: Acceso exitoso con credenciales válidas
    When ingreso el usuario "standard_user"
    And ingreso la contraseña "secret_sauce"
    And presiono el botón "Login"
    Then debería ver la página "Products"
    And el ícono del carrito debería estar visible

  @TC-02 @error
  Scenario: Acceso rechazado para un usuario bloqueado
    When ingreso el usuario "locked_out_user"
    And ingreso la contraseña "secret_sauce"
    And presiono el botón "Login"
    Then debería ver el mensaje "Epic sadface: Sorry, this user has been locked out."
    But no debería acceder al catálogo
```

## Feature 2: Checkout

```gherkin
Feature: Datos del comprador en el checkout
  Como cliente con productos en el carrito
  Quiero que el sistema valide mis datos de envío
  Para que la orden se registre correctamente

  Background:
    Given que inicié sesión con el usuario "standard_user"

  @TC-04 @error
  Scenario Outline: Checkout con un campo obligatorio vacío
    Given que agregué "Sauce Labs Backpack" al carrito
    And estoy en la página "Checkout: Your Information"
    When completo First Name "<nombre>", Last Name "<apellido>" y Postal Code "<código>"
    And presiono el botón "Continue"
    Then debería ver el mensaje "<mensaje>"
    And debería permanecer en la página "Checkout: Your Information"

    Examples:
      | nombre | apellido | código | mensaje                        |
      |        |          |        | Error: First Name is required  |
      | Ana    |          |        | Error: Last Name is required   |
      | Ana    | Quispe   |        | Error: Postal Code is required |

  @exitoso
  Scenario: Compra completada con un producto
    Given que agregué "Sauce Labs Backpack" al carrito
    When completo el checkout con First Name "Ana", Last Name "Quispe" y Postal Code "0000"
    And presiono el botón "Finish"
    Then debería ver el mensaje "Thank you for your order!"
    And el carrito debería quedar vacío

  @TC-05 @BUG-01-F @error
  Scenario: No se permite comprar con el carrito vacío
    Given que mi carrito no tiene productos
    When abro el carrito
    Then el botón "Checkout" debería estar deshabilitado
    But no debería registrarse ninguna orden
```

## Relación con los casos de prueba

| Escenario | Caso | Resultado de la ejecución |
|-----------|------|---------------------------|
| Acceso exitoso con credenciales válidas | TC-01 | Passed |
| Acceso rechazado para un usuario bloqueado | TC-02 | Passed |
| Checkout con un campo obligatorio vacío (3 filas) | TC-04 | Passed |
| Compra completada con un producto | Flujo de referencia | No forma parte de los 5 casos |
| No se permite comprar con el carrito vacío | TC-05 | Failed — BUG-01-F |
