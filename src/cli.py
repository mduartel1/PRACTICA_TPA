from src.services import gestor_tareas


def menu_tareas():
    while True:
        print("\n=== Gestor de Tareas ===")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Marcar como completada")
        print("4. Eliminar tarea")
        print("5. Salir")
        opcion = input("> ").strip()

        if opcion == "1":
            titulo = input("Título: ").strip()
            desc = input("Descripción: ").strip()
            prioridad = (
                input("Prioridad [baja|media|alta] (default: media): ").strip()
                or "media"
            )
            nueva = gestor_tareas.agregar_tarea(titulo, desc, prioridad)
            print(f"Creada tarea [{nueva.id}] {nueva.titulo}")
        elif opcion == "2":
            tareas = gestor_tareas.listar_tareas()
            if not tareas:
                print("No hay tareas.")
            for t in tareas:
                estado = "✅" if t.completada else "❌"
                print(f"[{t.id}] {t.titulo} - {t.prioridad} {estado}")
        elif opcion == "3":
            try:
                id_t = int(input("ID de tarea a completar: "))
                ok = gestor_tareas.marcar_completada(id_t)
                print("Marcada." if ok else "ID no encontrado.")
            except ValueError:
                print("ID inválido.")
        elif opcion == "4":
            try:
                id_t = int(input("ID de tarea a eliminar: "))
                ok = gestor_tareas.eliminar_tarea(id_t)
                print("Eliminada." if ok else "ID no encontrado.")
            except ValueError:
                print("ID inválido.")
        elif opcion == "5":
            break
        else:
            print("Opción inválida.")
