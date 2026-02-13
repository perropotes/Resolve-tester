# Task Helper Skeleton / Esqueleto con Helpers para Tareas

## English
This repository now follows a **modular structure** so `main` stays clean and each task-related behavior lives in a dedicated helper.

### Structure
- `main.py`: entry point, only orchestration.
- `helpers/tasks.py`: helper functions for task retrieval and formatting.

### Run
1. Ensure Python 3.10+ is installed.
2. Run:
   ```bash
   python3 main.py
   ```

### Why this structure?
Keeping helper logic outside `main` makes it easier to add new behaviors without creating spaghetti code.

---

## Español
Este repositorio ahora sigue una **estructura modular** para que `main` se mantenga limpio y cada comportamiento relacionado con tareas viva en un helper dedicado.

### Estructura
- `main.py`: punto de entrada, solo orquestación.
- `helpers/tasks.py`: funciones helper para obtener y formatear tareas.

### Pasos para ejecutar
1. Asegúrate de tener Python 3.10+ instalado.
2. Ejecuta:
   ```bash
   python3 main.py
   ```

### ¿Por qué esta estructura?
Mantener la lógica en helpers fuera de `main` facilita agregar nuevas funciones sin convertir el código en código espagueti.
