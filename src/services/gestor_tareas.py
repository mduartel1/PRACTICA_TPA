from src.models.tarea import Tarea
from src.storage.database import get_conn
from src.utils.logging_config import logger


def listar_tareas():
    """Devuelve la lista de tareas desde la base de datos SQLite."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, titulo, descripcion, prioridad, completada "
            "FROM tareas ORDER BY id;"
        )
        filas = cur.fetchall()
        conn.close()

        tareas = [
            Tarea(id_, titulo, desc, prio, bool(comp))
            for (id_, titulo, desc, prio, comp) in filas
        ]
        logger.info(f"Se listaron {len(tareas)} tareas.")
        return tareas

    except Exception as e:
        logger.error("Error al listar tareas", exc_info=True)
        raise e


def agregar_tarea(titulo, descripcion, prioridad="media"):
    """Agrega una nueva tarea a la base de datos."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tareas (titulo, descripcion, prioridad, completada) "
            "VALUES (?, ?, ?, 0);",
            (titulo, descripcion, prioridad),  # ✅ Se pasan los 3 valores
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()

        logger.info(f"Tarea creada: '{titulo}' (id={new_id}, prioridad={prioridad})")
        return Tarea(new_id, titulo, descripcion, prioridad, False)

    except Exception as e:
        logger.error("Error al agregar tarea", exc_info=True)
        raise e


def marcar_completada(id_tarea):
    """Marca una tarea como completada."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE tareas SET completada=1 WHERE id=?;", (id_tarea,))
        ok = cur.rowcount > 0
        conn.commit()
        conn.close()

        if ok:
            logger.info(f"Tarea marcada como completada (id={id_tarea})")
        else:
            logger.warning(f"Tarea no encontrada (id={id_tarea})")

        return ok

    except Exception as e:
        logger.error("Error al marcar tarea como completada", exc_info=True)
        raise e


def eliminar_tarea(id_tarea):
    """Elimina una tarea de la base de datos."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM tareas WHERE id=?;", (id_tarea,))
        ok = cur.rowcount > 0
        conn.commit()
        conn.close()

        if ok:
            logger.info(f"Tarea eliminada (id={id_tarea})")
        else:
            logger.warning(f"Tarea no encontrada (id={id_tarea})")

        return ok

    except Exception as e:
        logger.error("Error al eliminar tarea", exc_info=True)
        raise e
