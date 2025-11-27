
from src.storage import persistencia


def test_guardar_y_cargar_tareas_json(tmp_path, monkeypatch):
    # Usar un fichero temporal para no tocar datos reales
    data_path = tmp_path / "tareas_test.json"
    monkeypatch.setattr(persistencia, "DATA_PATH", data_path)

    tareas = [
        {
            "id": 1,
            "titulo": "T1",
            "descripcion": "D1",
            "prioridad": "alta",
            "completada": False,
        },
        {
            "id": 2,
            "titulo": "T2",
            "descripcion": "D2",
            "prioridad": "media",
            "completada": True,
        },
    ]

    persistencia.guardar_tareas(tareas)
    assert data_path.exists()

    cargadas = persistencia.cargar_tareas()
    assert cargadas == tareas
