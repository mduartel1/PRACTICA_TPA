from src.models.tarea import Tarea
from src.storage.persistencia import cargar_tareas, guardar_tareas


def listar_tareas():
    return [Tarea.from_dict(t) for t in cargar_tareas()]


def _nuevo_id(tareas_dict):
    # IDs consecutivos simples (suficiente para PRAC2)
    return (max([t["id"] for t in tareas_dict]) + 1) if tareas_dict else 1


def agregar_tarea(titulo, descripcion, prioridad="media"):
    tareas = cargar_tareas()
    nueva = Tarea(_nuevo_id(tareas), titulo, descripcion, prioridad)
    tareas.append(nueva.to_dict())
    guardar_tareas(tareas)
    return nueva


def marcar_completada(id_tarea):
    tareas = cargar_tareas()
    for t in tareas:
        if t["id"] == id_tarea:
            t["completada"] = True
            guardar_tareas(tareas)
            return True
    return False


def eliminar_tarea(id_tarea):
    tareas = cargar_tareas()
    nuevas = [t for t in tareas if t["id"] != id_tarea]
    if len(nuevas) != len(tareas):
        guardar_tareas(nuevas)
        return True
    return False
