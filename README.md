# Examen Práctico Hito 3 — Testing & Quality Assurance

Pruebas funcionales y estructurales aplicadas sobre la aplicación de demostración **SauceDemo (Swag Labs)**.

**URL probada:** https://www.saucedemo.com/

## Resumen de resultados

| Actividad | Resultado |
|-----------|-----------|
| Caja negra | 5 casos ejecutados: 4 Passed, 1 Failed |
| Bugs | 1 defecto reproducible (BUG-01-F: compra completada con el carrito vacío) |
| Caja blanca | Criterio de decisiones: mínimo 4 casos. Los 3 casos diseñados cubren 87.5 % de sentencias y 83.3 % de decisiones; se agrega CB-04 para llegar al 100 % |
| Gherkin | 2 features, 5 escenarios (exitosos y de error) |

## Estructura

```
Examen-Hito-3-TQA/
├── README.md
├── docs/
│   ├── casos_caja_negra.md        # TC-01 a TC-05 con resultados
│   ├── analisis_caja_blanca.md    # decisiones, criterio, mínimo de casos, ajuste
│   └── escenarios_gherkin.md      # escenarios BDD
├── bugs/
│   └── bugs_encontrados.md        # BUG-01-F
├── caja_blanca/
│   ├── validar_compra.py          # código del examen
│   └── test_validar_compra.py     # casos CB-01 a CB-05
├── evidencias/
│   ├── capturas/                  # capturas de cada caso
│   ├── ejecutar_casos_saucedemo.py
│   └── cobertura_caja_blanca.txt
└── entregable/
    ├── informe_hito3.docx
    └── informe_hito3.pdf
```

## Cómo repetir la ejecución

Caja negra (requiere `pip install playwright` y `python -m playwright install chromium`):

```
python evidencias/ejecutar_casos_saucedemo.py evidencias/capturas
```

Caja blanca con cobertura de ramas (requiere `pip install pytest coverage`):

```
cd caja_blanca
python -m coverage run --branch -m pytest -m tres   # solo los 3 casos
python -m coverage report -m
python -m coverage run --branch -m pytest           # con el ajuste
python -m coverage report -m
```
