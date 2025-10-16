class Tarea:
    """
    Representa una tarea con título, descripción, prioridad y estado.
    """

    def __init__(self, id, titulo, descripcion, prioridad="media", completada=False):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.completada = completada

    def marcar_completada(self):
        self.completada = True

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "completada": self.completada,
        }

    @staticmethod
    def from_dict(data):
        return Tarea(
            data["id"],
            data["titulo"],
            data["descripcion"],
            data.get("prioridad", "media"),
            data.get("completada", False),
        )
