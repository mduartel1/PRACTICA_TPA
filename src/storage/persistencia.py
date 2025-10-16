import json
from pathlib import Path

DATA_PATH = Path("data/tareas.json")


def cargar_tareas():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_tareas(tareas):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)
