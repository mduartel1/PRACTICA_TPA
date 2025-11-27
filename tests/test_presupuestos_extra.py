from src.storage.database import get_conn, init_db
from src.services import gestor_presupuestos as gp


def limpiar_tabla_presupuestos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM presupuestos;")
    conn.commit()
    conn.close()


def setup_function(_):
    # DB inicializada por conftest; aquí solo limpiamos la tabla
    init_db()
    gp.crear_tabla()
    limpiar_tabla_presupuestos()


def test_agregar_y_listar_presupuestos():
    gp.agregar_presupuesto("Sueldo", 1200, "ingreso")
    gp.agregar_presupuesto("Alquiler", 800, "gasto")

    datos = gp.listar_presupuestos()

    assert len(datos) == 2
    conceptos = {fila[1] for fila in datos}
    assert "Sueldo" in conceptos
    assert "Alquiler" in conceptos


def test_eliminar_presupuesto():
    gp.agregar_presupuesto("Sueldo", 1200, "ingreso")
    gp.agregar_presupuesto("Alquiler", 800, "gasto")

    datos = gp.listar_presupuestos()
    ids = [fila[0] for fila in datos]
    primer_id = ids[0]

    ok = gp.eliminar_presupuesto(primer_id)
    assert ok is True

    datos_restantes = gp.listar_presupuestos()
    ids_restantes = {fila[0] for fila in datos_restantes}

    assert primer_id not in ids_restantes
    assert len(datos_restantes) == 1