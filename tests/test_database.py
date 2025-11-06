from src.storage.database import get_conn, init_db


def test_init_db_crea_tablas():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tareas';")
    row = cur.fetchone()
    conn.close()
    assert row is not None
