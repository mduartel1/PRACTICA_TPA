from src.services import gestor_presupuestos as gp
from src.storage.database import init_db


def setup_module(_):
    init_db()
    gp.crear_tabla()


def test_insertar_y_listar_presupuesto():
    gp.agregar_presupuesto("Sueldo", 1200, "ingreso")
    datos = gp.listar_presupuestos()
    assert any(d[1] == "Sueldo" and float(d[2]) == 1200 for d in datos)
