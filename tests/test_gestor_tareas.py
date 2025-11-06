from src.services import gestor_tareas
from src.storage.database import get_conn, init_db


def limpiar_tabla():
    """Borra todas las tareas de la base de datos antes de cada test."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas;")
    conn.commit()
    conn.close()


def setup_function(_):
    """Se ejecuta antes de cada test para asegurar una DB limpia."""
    init_db()
    limpiar_tabla()


def test_agregar_y_listar():
    gestor_tareas.agregar_tarea("T1", "Desc1", "alta")
    gestor_tareas.agregar_tarea("T2", "Desc2", "media")

    tareas = gestor_tareas.listar_tareas()

    assert len(tareas) == 2
    assert tareas[1].titulo == "T2"  # ✅ comprobamos el orden, no el ID


def test_marcar_completada():
    t = gestor_tareas.agregar_tarea("T1", "Desc1")
    ok = gestor_tareas.marcar_completada(t.id)
    assert ok is True

    tareas = gestor_tareas.listar_tareas()
    assert tareas[0].completada is True


def test_eliminar():
    t = gestor_tareas.agregar_tarea("T1", "Desc1")
    ok = gestor_tareas.eliminar_tarea(t.id)
    assert ok is True

    tareas = gestor_tareas.listar_tareas()
    assert len(tareas) == 0
