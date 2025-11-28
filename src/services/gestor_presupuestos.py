from src.storage.database import get_conn
from src.utils.logging_config import logger


def crear_tabla():
    """Crea la tabla de presupuestos si no existe."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS presupuestos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concepto TEXT NOT NULL,
                monto REAL NOT NULL,
                tipo TEXT CHECK(tipo IN ('ingreso','gasto')) NOT NULL
            );
        """
        )
        conn.commit()
        conn.close()
        logger.info(
            "Tabla 'presupuestos' verificada o creada exitosamente."
        )  # ✅ Registro
    except Exception as e:
        logger.error("Error al crear/verificar la tabla de presupuestos", exc_info=True)
        raise e


def agregar_presupuesto(concepto, monto, tipo):
    """Agrega un nuevo presupuesto (ingreso o gasto)."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO presupuestos (concepto, monto, tipo) VALUES (?, ?, ?);",
            (concepto, float(monto), tipo),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()

        logger.info(
            f"Presupuesto agregado: '{concepto}' ({tipo}, monto={monto}, id={new_id})"
        )  # ✅ Registro
        return new_id

    except Exception as e:
        logger.error("Error al agregar presupuesto", exc_info=True)
        raise e


def listar_presupuestos():
    """Devuelve todos los presupuestos registrados."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, concepto, monto, tipo FROM presupuestos ORDER BY id;")
        datos = cur.fetchall()
        conn.close()

        logger.info(f"Se listaron {len(datos)} presupuestos.")  # ✅ Registro
        return datos

    except Exception as e:
        logger.error("Error al listar presupuestos", exc_info=True)
        raise e


def eliminar_presupuesto(id_presupuesto):
    """Elimina un presupuesto por ID."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM presupuestos WHERE id=?;", (id_presupuesto,))
        ok = cur.rowcount > 0
        conn.commit()
        conn.close()

        if ok:
            logger.info(f"Presupuesto eliminado (id={id_presupuesto})")  # ✅ Registro
        else:
            logger.warning(f"Presupuesto no encontrado (id={id_presupuesto})")

        return ok

    except Exception as e:
        logger.error("Error al eliminar presupuesto", exc_info=True)
        raise e
