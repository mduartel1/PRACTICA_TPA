from __future__ import annotations

import sqlite3
from typing import List, Tuple, Any

from src.storage.database import get_conn


def listar_inventario() -> List[Tuple[int, str, int, float]]:
    """Devuelve una lista de items del inventario."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, cantidad, precio FROM inventario ORDER BY id;")
    filas = cursor.fetchall()
    conn.close()
    return filas


def agregar_item(nombre: str, cantidad: int, precio: float) -> bool:
    """Agrega un nuevo item al inventario."""
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO inventario (nombre, cantidad, precio) VALUES (?, ?, ?);",
            (nombre, cantidad, precio),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def actualizar_cantidad(item_id: int, cantidad: int) -> bool:
    """Actualiza la cantidad de un item. Devuelve True si se modificó."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventario SET cantidad = ? WHERE id = ?;", (cantidad, item_id))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success


def eliminar_item(item_id: int) -> bool:
    """Elimina un item por ID. Devuelve True si se eliminó."""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventario WHERE id = ?;", (item_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success
