import pytest
from validar_compra import validar_compra

# Casos CB-01 a CB-03: los tres casos pedidos en el examen
TRES_CASOS = [
    ("CB-01", 16, True, 500, 100, "Compra no permitida: edad"),
    ("CB-02", 25, False, 500, 100, "Compra no permitida: cuenta"),
    ("CB-03", 25, True, 500, 100, "Compra aprobada"),
]

# Ajuste: CB-04 completa decisiones; CB-05 completa condiciones con cortocircuito
AJUSTE = [
    ("CB-04", 25, True, 50, 100, "Compra rechazada"),
    ("CB-05", 25, True, 500, 0, "Compra rechazada"),
]


@pytest.mark.tres
@pytest.mark.parametrize("cid,edad,activa,saldo,monto,esperado", TRES_CASOS)
def test_tres_casos(cid, edad, activa, saldo, monto, esperado):
    assert validar_compra(edad, activa, saldo, monto) == esperado


@pytest.mark.parametrize("cid,edad,activa,saldo,monto,esperado", AJUSTE)
def test_ajuste(cid, edad, activa, saldo, monto, esperado):
    assert validar_compra(edad, activa, saldo, monto) == esperado
