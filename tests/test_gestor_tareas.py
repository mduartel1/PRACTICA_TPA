from src.services import gestor_tareas
from src.storage import persistencia


def setup_function(_):
    # Limpia el archivo de datos antes de cada test
    if persistencia.DATA_PATH.exists():
        persistencia.DATA_PATH.unlink()
    persistencia.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)


def test_agregar_y_listar():
    gestor_tareas.agregar_tarea("T1", "Desc1", "alta")
    gestor_tareas.agregar_tarea("T2", "Desc2", "media")
    tareas = gestor_tareas.listar_tareas()
    assert len(tareas) == 2
    assert tareas[0].id == 1
    assert tareas[1].titulo == "T2"


def test_marcar_completada():
    gestor_tareas.agregar_tarea("T1", "Desc1")
    ok = gestor_tareas.marcar_completada(1)
    assert ok is True
    assert gestor_tareas.listar_tareas()[0].completada is True


def test_eliminar():
    gestor_tareas.agregar_tarea("T1", "Desc1")
    ok = gestor_tareas.eliminar_tarea(1)
    assert ok is True
    assert len(gestor_tareas.listar_tareas()) == 0
