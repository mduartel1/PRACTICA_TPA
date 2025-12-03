# CHANGELOG – PRACTICA_TPA

Este documento recoge los cambios realizados en el proyecto a lo largo de su desarrollo para la asignatura **Técnicas de Programación Avanzada**.

---

## v1.0.0 – PRAC4 (Versión Final)
**Fecha:** 23/11/2025

### Añadido
- README final completamente ampliado (más de 200 líneas), con diagramas PRAC2–PRAC3 y documentación final PRAC4.
- Test de integración CLI → SQLite.
- Ampliación de las pruebas unitarias para alcanzar cobertura ≥ 70%.
- Sección conceptual de Inventario incluida en el CLI y en la documentación.
- Documentación pdoc revisada y actualizada para todos los módulos.
- Informe PRAC4 generado en formatos PDF y DOCX.
- Implementación completa del módulo de Inventario sobre SQLite, accesible desde CLI y GUI.
- Nueva GUI profesional desarrollada con PySide6, incluyendo pestañas, tablas, diálogos modales y estilos modernos.

### Mejorado
- Organización interna del repositorio.
- Arquitectura documentada de manera completa.
- Logging profesional en todo el proyecto.
- Estructura de los tests y limpieza automática de tablas.
- CI/CD totalmente estable y validado.
- Sustitución del CLI como interfaz principal por una GUI más accesible para el usuario.

### Corregido
- Errores de formato detectados por Black y Ruff.
- Inconsistencias de estilo en tests de integración y persistencia.
- Problemas de importación y rutas en algunos módulos durante el CI.
- Problemas de estilo y coherencia en la interfaz gráfica resueltos.

---

## v0.3.0 – PRAC3
**Fecha:** 23/11/2025

### Añadido
- Migración completa de JSON a SQLite para tareas y presupuestos.
- Logging centralizado.
- Creación del módulo de presupuestos.
- Cobertura inicial > 55%.
- Diagrama de arquitectura PRAC3.

### Mejorado
- Refactor general del proyecto.
- Tablas SQLite creadas automáticamente al iniciar el sistema.

---

## v0.2.0 – PRAC2
- Implementación del módulo de tareas.
- Diagrama de clases, paquetes y secuencia (PRAC2).
- CLI básico y lectura/escritura con archivo JSON.

---

## v0.1.0 – Inicio de proyecto
- Estructura inicial del repositorio.
- Primeras clases y módulos base.