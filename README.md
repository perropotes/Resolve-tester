# Resolve tester scripts

## Nuevo helper: `textplus_multi_intro_helper.lua`

Ruta: `Scripts/Edit/textplus_multi_intro_helper.lua`

### Objetivo
Aplicar animaciones de entrada a múltiples elementos **Text+** seleccionados en la línea de tiempo (página Edit), con variación por elemento y límite de 20 clips.

### Comportamiento
- Usa los clips seleccionados en timeline (`GetSelectedItems()`), con fallback al clip de video actual.
- Filtra solo clips que tengan al menos un nodo `TextPlus` dentro de su Fusion Comp.
- Distribuye posiciones finales en una grilla para evitar que se tapen entre sí.
- Aplica entrada de 6 frames por clip.
- Perfiles base:
  1. Sube desde abajo + fade in.
  2. Glitch de opacidad irregular y final en 100%.
  3. Entra desde la izquierda + fade in.
  4. Pop de escala + fade in.
  5. Micro-rotación + ajuste de posición + fade in.
- Si hay más de 5 elementos, los perfiles se repiten aleatoriamente.

### Uso
1. Selecciona en Edit los clips Text+ que quieres animar.
2. Ejecuta el script desde el menú de scripts de Resolve.
3. Revisa la consola para ver cuántos clips se procesaron y con qué perfil.

### Nota
La API pública de Resolve/Fusion cambia entre versiones. El helper incluye defensas (`pcall`) para no romper si una propiedad no está disponible.
