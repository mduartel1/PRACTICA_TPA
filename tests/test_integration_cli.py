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
    - Simula un usuario que entra al menú,
      agrega una tarea y luego sale.
    - Verifica que la tarea quedó almacenada.
    """
    init_db()
    limpiar_tabla_tareas()

    # Secuencia de inputs simulados
    inputs = iter(
        [
            "1",               # menú: agregar tarea
            "Tarea PRAC4",     # título
            "Desc PRAC4",      # descripción
            "alta",            # prioridad
            "5",               # menú: salir
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from src.cli import menu_tareas

    menu_tareas()  # corre CLI

    tareas = gestor_tareas.listar_tareas()
    titulos = [t.titulo for t in tareas]
    assert "Tarea PRAC4" in titulos