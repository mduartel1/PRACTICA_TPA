from src.storage.database import get_conn, init_db
from src.services import gestor_tareas


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
    - Verifica que la tarea quedó almacenada en la base de datos.
    """
    init_db()
    limpiar_tabla_tareas()

    # Secuencia de inputs simulados para el menú:
    # 1) opción "Agregar tarea"
    # 2) título, descripción, prioridad
    # 3) opción "Salir"
    inputs = iter(
        [
            "1",                 # menú: agregar tarea
            "Tarea PRAC4",       # título
            "Desc PRAC4",        # descripción
            "alta",              # prioridad
            "5",                 # menú: salir
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    from src.cli import menu_tareas

    menu_tareas()  # si no lanza excepción, la CLI ha funcionado

    tareas = gestor_tareas.listar_tareas()
    titulos = [t.titulo for t in tareas]
    assert "Tarea PRAC4" in titulos