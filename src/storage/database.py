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
            prioridad TEXT DEFAULT 'media',
            completada INTEGER DEFAULT 0
        );
    """
    )
    conn.commit()
    conn.close()


def get_conn():
    return sqlite3.connect(DB_PATH)
