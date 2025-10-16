from src.models.tarea import Tarea


def test_marcar_completada():
    t = Tarea(1, "Probar", "Hacer test")
    t.marcar_completada()
    assert t.completada is True


def test_to_from_dict():
    t = Tarea(1, "X", "Y", "alta", False)
    d = t.to_dict()
    t2 = Tarea.from_dict(d)
    assert t2.titulo == "X"
    assert t2.prioridad == "alta"
    assert t2.completada is False
