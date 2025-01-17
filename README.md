# SongSearch

**Versión Actual**: Alpha 1.0

SongSearch es una herramienta diseñada para facilitar la gestión y búsqueda de canciones en bibliotecas de música grandes. La aplicación permite buscar canciones o artistas en carpetas seleccionadas, comparar listas personalizadas con los archivos disponibles, y exportar los resultados para integrarlos en herramientas como Rekordbox.

---

## **Características**
- **Búsqueda Avanzada**: Analiza carpetas configuradas y compara nombres de canciones con las entradas proporcionadas por el usuario.
- **Interfaz de Usuario**:
  - Selección de parámetros de búsqueda como tipo de archivo e intensidad.
  - Resultados visuales con archivos encontrados (verde) y no encontrados (rojo).
  - Opción para seleccionar carpetas y actualizar la base de datos.
- **Exportación de Resultados**: Permite guardar resultados en archivos `.txt` o `.csv`.
- **Integración con Rekordbox** (pendiente de implementación).
- **Multiplataforma**: Compatible con Windows y macOS.

---

## **Requisitos del Sistema**
- **Python**: 3.8 o superior
- **Dependencias**:
  - `PyQt5`
  - `rapidfuzz`

---

## **Instalación**
1. Clona este repositorio en tu máquina:
   ```bash
   git clone https://github.com/WhiteTrackProject/SongSearch.git
   cd SongSearch

2. Crea y activa un entorno virtual:
    python -m venv venv
    # En Windows:
    .\\venv\\Scripts\\activate
    # En macOS/Linux:
    source venv/bin/activate

3. Instala dependencias:
    pip install -r requirements.txt

4. Ejecuta la app:
    python src/app.py


Planes Futuros
Integración con Rekordbox:

Crear listas de reproducción automáticamente basadas en los resultados.
Mejora del Rendimiento:

Optimizar la búsqueda en carpetas grandes.
Mostrar resultados en tiempo real.
Interfaz Mejorada:

Añadir temas personalizados.
Mejorar la visualización de resultados.
Exportación Detallada:

Opción para exportar resultados faltantes y encontrados.
