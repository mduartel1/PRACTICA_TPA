# PRACTICA_TPA
![CI](https://github.com/mduartel1/PRACTICA_TPA/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/mduartel1/PRACTICA_TPA/branch/main/graph/badge.svg)](https://codecov.io/gh/mduartel1/PRACTICA_TPA)

# Gestor CLI de Tareas, Presupuestos e Inventario

Proyecto desarrollado para la asignatura **Técnicas de Programación Avanzada**.
Incluye CLI, persistencia JSON, pruebas unitarias y CI automatizada con GitHub Actions.

## Documentacion Automatica

La documentacion se genera con [pdoc](hhtps://pdoc.dev):

## Arquitectura (PRAC2)

### Diagrama de clases
```mermaid
classDiagram
    direction LR

    class Tarea {
      +int id
      +str titulo
      +str descripcion
      +str prioridad
      +bool completada
      +marcar_completada()
      +to_dict() dict
      +from_dict(data) Tarea
    }

    class GestorTareas {
      +listar_tareas() list~Tarea~
      +agregar_tarea(titulo, descripcion, prioridad="media") Tarea
      +marcar_completada(id_tarea) bool
      +eliminar_tarea(id_tarea) bool
      -_nuevo_id(tareas_dict) int
    }

    class Persistencia {
      <<module>>
      +cargar_tareas() list~dict~
      +guardar_tareas(tareas:list~dict~) void
      -DATA_PATH
    }

    class CLI {
      <<module>>
      +menu_tareas() void
    }

    class Main {
      <<module>>
      +main() void
    }

    GestorTareas --> Tarea : crea/retorna
    GestorTareas --> Persistencia : usa
    CLI --> GestorTareas : invoca
    Main --> CLI : arranca menú
```

**Explicación:**  
El diagrama de clases muestra la estructura lógica del módulo de Tareas.  
Define las relaciones entre las clases `Tarea`, `GestorTareas`, `Persistencia`, `CLI` y `Main`, destacando cómo `GestorTareas` coordina las operaciones de creación y persistencia de datos.

### Diagrama de paquetes
```mermaid
graph LR
  A[src/] --> B[models/]
  A[src/] --> C[services/]
  A[src/] --> D[storage/]
  A[src/] --> E[cli.py]
  A[src/] --> F[main.py]

  B --> B1[tarea.py]
  C --> C1[gestor_tareas.py]
  D --> D1[persistencia.py]
```

**Explicación:**  
Este diagrama representa la organización modular del proyecto.  
Cada carpeta contiene responsabilidades bien definidas: `models` para las entidades, `services` para la lógica de negocio, y `storage` para la persistencia, mientras que `cli.py` y `main.py` gestionan la interfaz de usuario y la ejecución principal.

### Flujo: agregar tarea
```mermaid
sequenceDiagram
    participant U as Usuario
    participant CLI as CLI.menu_tareas()
    participant S as services.gestor_tareas
    participant P as storage.persistencia
    participant M as models.Tarea

    U->>CLI: opción "Agregar"
    CLI->>S: agregar_tarea(titulo, desc, prioridad)
    S->>P: cargar_tareas()
    P-->>S: lista de dicts
    S->>M: Tarea(...)
    S->>P: guardar_tareas(tareas+1)
    S-->>CLI: Tarea creada (id)
    CLI-->>U: "Creada tarea [id]"
```

**Explicación:**  
El diagrama de secuencia describe el flujo de interacción cuando un usuario agrega una tarea.  
Muestra cómo las llamadas entre `CLI`, `GestorTareas`, `Persistencia` y `Tarea` cooperan para almacenar la información y devolver una confirmación al usuario.
