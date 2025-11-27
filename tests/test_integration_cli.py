from src.services import gestor_tareas
from src.storage.database import get_conn, init_db


def limpiar_tabla_tareas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas;")
    conn.commit()
    conn.close()


def test_flujo_completo_cli_agregar_y_listar(monkeypatch, capsys):
    """
    Test de integración:
    - Simula el menú CLI.
    - Agrega una tarea.
    - Comprueba su existencia en SQLite.
    """
    init_db()
    limpiar_tabla_tareas()

    inputs = iter(
        [
            "1",  # agregar tarea
            "Tarea PRAC4",
            "Desc PRAC4",
            "alta",
            "5",  # salir
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from src.cli import menu_tareas

    menu_tareas()

    tareas = gestor_tareas.listar_tareas()
    titulos = [t.titulo for t in tareas]
    assert "Tarea PRAC4" in titulos
