# My Calendar (FastHTML)

Calendario mensual con HTMX/FastHTML y SQLite, pensado para gestionar categorias con emoji y eventos rapidos desde modales.

## Caracteristicas
- Vista mensual con navegacion de meses y resaltado del dia actual.
- Filtro por categoria y pagina dedicada para crear/eliminar categorias (emoji + color).
- Modal por dia para listar, agregar y borrar eventos sin recargar.
- Selector de idioma (en/es) y cambio de tema claro/oscuro persistido en `localStorage`.
- Datos persistentes en `calendar.db` (SQLite) manejados via fastlite.

## Requisitos
- Python 3.10+.
- Dependencias pip: `fasthtml` (incluye Starlette, HTMX, fastlite). No hay `requirements.txt`; instala manualmente.

## Instalacion y ejecucion
```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install fasthtml
python main.py              # Servira en http://localhost:5001 (autoreload activado por live=True)
```

`calendar.db` se crea si no existe. Borra el archivo para reiniciar datos.

## Uso rapido
- Vista principal (`/`): navegar meses, filtrar por categoria, cambiar idioma/tema. Click en un dia abre modal para eventos.
- Modal de dia: selecciona categoria, agrega nota opcional y envia; HTMX actualiza la lista y el calendario con `hx-swap-oob`.
- Categorias (`/categories`): crea nuevas categorias (emoji picker + color) o elimina existentes. Boton "Volver" regresa al calendario.

## Estructura del proyecto
- `main.py`: toda la logica de rutas, componentes HTMX y creacion de tablas `categories`/`events`.
- `assets/styles.css`: tema light/dark, layout del calendario, modales y controles.
- `assets/scripts.js`: manejo de modal HTMX, emoji picker, toggles de tema e idioma, atajos de teclado (Escape).
- `calendar.db`: base de datos SQLite con tablas `categories` y `events`.
- `context/llms-ctx*.txt`: referencia de FastHTML incluida para el entorno de IA.

## Notas de implementacion
- El idioma se guarda en sesion (`lang`), por defecto `'es'`. El re-render HTMX de eventos usa idioma fijo `"es"`; ajusta los handlers de `/events` si necesitas reflejar el idioma activo.
- Los assets se sirven via `/assets/{fname:path}`; no hay pipeline de build.
- No hay pruebas automatizadas ni configuracion de despliegue; agrega segun sea necesario.
