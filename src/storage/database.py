import sqlite3
from pathlib import Path

DB_PATH = Path("data/gestor.db")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            prioridad TEXT,
            completada INTEGER DEFAULT 0
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL,
            tipo TEXT NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL DEFAULT 0.0
        );
        """
    )
    conn.commit()
    conn.close()


def get_conn():
    return sqlite3.connect(DB_PATH)
