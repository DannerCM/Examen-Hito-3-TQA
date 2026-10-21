# Análisis de caja blanca — `validar_compra`

## Código analizado

```python
def validar_compra(edad, cuenta_activa, saldo, monto):
    if edad < 18:                          # D1
        return "Compra no permitida: edad"   # S1
    if not cuenta_activa:                  # D2
        return "Compra no permitida: cuenta" # S2
    if saldo >= monto and monto > 0:       # D3
        return "Compra aprobada"             # S3
    return "Compra rechazada"                # S4
```

El archivo está en `caja_blanca/validar_compra.py` y los casos se ejecutan con `caja_blanca/test_validar_compra.py`.

## 1. Decisiones y condiciones simples

| Decisión | Expresión | Condiciones simples |
|----------|-----------|---------------------|
| D1 | `edad < 18` | C1: `edad < 18` |
| D2 | `not cuenta_activa` | C2: `cuenta_activa` (la decisión es verdadera cuando C2 es falsa) |
| D3 | `saldo >= monto and monto > 0` | C3: `saldo >= monto`; C4: `monto > 0` |

Son 3 decisiones, 4 condiciones simples, 4 sentencias `return` (S1 a S4) y 8 sentencias en total contando los tres `if`.

## 2. Criterio utilizado

Se usa **cobertura de decisiones**: cada decisión debe tomar al menos una vez su resultado verdadero y su resultado falso. Este criterio incluye a la cobertura de sentencias, porque recorrer ambas salidas de cada `if` obliga a ejecutar los cuatro `return`.

## 3. Mínimo de casos y cálculo

Las tres decisiones van en secuencia y cada salida verdadera termina la función con un `return`. Por eso un caso no puede cubrir dos salidas verdaderas a la vez:

- D1 verdadera termina en S1: 1 caso propio.
- D2 verdadera exige D1 falsa y termina en S2: 1 caso propio.
- D3 necesita llegar con D1 y D2 falsas, y debe salir una vez verdadera (S3) y otra falsa (S4): 2 casos.

**Mínimo para cobertura de decisiones = 1 + 1 + 2 = 4 casos.** Coincide con el número de caminos independientes (3 decisiones + 1 = 4) y con el número de `return`, ya que cada uno es un camino que termina distinto.

## 4. Los 3 casos diseñados

| Caso | edad | cuenta_activa | saldo | monto | Resultado esperado | Cubre |
|------|------|---------------|-------|-------|--------------------|-------|
| CB-01 | 16 | True | 500 | 100 | Compra no permitida: edad | D1 = V (S1) |
| CB-02 | 25 | False | 500 | 100 | Compra no permitida: cuenta | D1 = F, D2 = V (S2) |
| CB-03 | 25 | True | 500 | 100 | Compra aprobada | D1 = F, D2 = F, D3 = V con C3 = V y C4 = V (S3) |

Los tres casos se ejecutaron y pasaron.

**Cobertura alcanzada con 3 casos**

| Criterio | Cubierto | Cobertura |
|----------|----------|-----------|
| Sentencias | 7 de 8 (falta S4) | 87.5 % |
| Decisiones (salidas) | 5 de 6 (falta D3 = F) | 83.3 % |
| Condiciones (valores V/F) | 6 de 8 (faltan C3 = F y C4 = F) | 75 % |

Detalle de condiciones: C1 toma V (CB-01) y F (CB-02); C2 toma F (CB-02) y V (CB-03); C3 y C4 solo toman V (CB-03).

coverage.py en modo ramas lo confirma: 8 sentencias con 1 sin ejecutar (línea 8, `return "Compra rechazada"`), 6 ramas con 1 parcial, 86 % combinado. La salida completa está en `evidencias/cobertura_caja_blanca.txt`.

## 5. Ajuste necesario

Los 3 casos **no alcanzan** la cobertura de decisiones porque D3 nunca sale falsa y S4 no se ejecuta. El cuarto caso que falta es:

| Caso | edad | cuenta_activa | saldo | monto | Resultado esperado | Cubre |
|------|------|---------------|-------|-------|--------------------|-------|
| CB-04 | 25 | True | 50 | 100 | Compra rechazada | D3 = F por C3 = F (S4) |

Con CB-01 a CB-04 se llega a 100 % de sentencias y 100 % de decisiones.

**Si el criterio fuera cobertura de condiciones**, falta además que C4 sea falsa. Python evalúa `and` con cortocircuito: si C3 es falsa, C4 ni siquiera se evalúa, así que CB-04 no sirve para C4. Hace falta un caso con C3 verdadera y C4 falsa:

| Caso | edad | cuenta_activa | saldo | monto | Resultado esperado | Cubre |
|------|------|---------------|-------|-------|--------------------|-------|
| CB-05 | 25 | True | 500 | 0 | Compra rechazada | C3 = V, C4 = F (D3 = F) |

Con los 5 casos coverage.py reporta 100 % en sentencias y ramas, y cada condición simple toma ambos valores.

## 6. Observación sobre valores límite

Tener 100 % de cobertura no garantiza que no haya defectos. Si el código tuviera `edad <= 18` en lugar de `edad < 18`, los casos anteriores (16 y 25) seguirían pasando con la misma cobertura. Para detectarlo conviene agregar valores límite:

| Valor límite | Entrada | Resultado esperado |
|--------------|---------|--------------------|
| Edad justo por debajo | edad 17 | Compra no permitida: edad |
| Edad en el límite | edad 18 | Sigue a la validación de cuenta |
| Saldo igual al monto | saldo 100, monto 100 | Compra aprobada |
| Monto mínimo positivo | saldo 100, monto 1 | Compra aprobada |
| Monto negativo | saldo 100, monto -5 | Compra rechazada |
