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
pip install -r requirements.txt
python main.py              # Servira en http://localhost:5001 (autoreload activado por live=True)
# Cambiar el puerto (ejemplo 5011): PORT=5011 python main.py
```

`calendar.db` se crea si no existe. Borra el archivo para reiniciar datos.
> Nota: `fasthtml` se instala desde GitHub (no esta en PyPI), por eso el `requirements.txt` usa una URL git.

## Uso rapido
- Vista principal (`/`): navegar meses, filtrar por categoria, cambiar idioma/tema. Click en un dia abre modal para eventos.
- Modal de dia: selecciona categoria, agrega nota opcional y envia; HTMX actualiza la lista y el calendario con `hx-swap-oob`.
- Categorias (`/categories`): crea nuevas categorias (emoji picker + color) o elimina existentes. Boton "Volver" regresa al calendario.

## Estructura del proyecto
- `main.py`: punto de entrada, solo arranca `serve()` usando la app modular.
- `app/`: logica principal separada.
  - `__init__.py`: construye `fast_app` con headers y registra rutas.
  - `routes.py`: controladores HTMX (home, categorias, modales de dias, CRUD de eventos) y assets estaticos. La cabecera se adapta: en desktop va en una sola linea (titulo | filtro + boton categorias | controles tema/idioma) y en movil muestra un boton “⋮” que despliega tema/idioma debajo del titulo.
  - `components.py`: componentes UI (`DayCell`, `LangSelector`, `ThemeToggle`, etc.).
  - `i18n.py`: traducciones y helpers de idioma/mes.
  - `db.py`: inicializa fastlite, crea tablas y expone dataclasses `Category` y `Event` (usa `data/calendar.db`).
- `assets/styles.css`: tema light/dark, layout del calendario, modales y controles; layout responsivo de cabecera (desktop linea unica, movil con boton de opciones y panel desplegable).
- `assets/scripts.js`: manejo de modal HTMX, emoji picker, toggles de tema e idioma, boton de opciones en movil, atajos de teclado (Escape).
- `data/calendar.db`: base de datos SQLite con tablas `categories` y `events` (se autogenera).
- `context/llms-ctx*.txt`: referencia de FastHTML incluida para el entorno de IA.

## Notas de implementacion
- El idioma se guarda en sesion (`lang`), por defecto `'es'`; los swaps OOB de eventos usan el idioma activo de la sesion.
- Los assets se sirven via `/assets/{fname:path}`; no hay pipeline de build.
- No hay pruebas automatizadas ni configuracion de despliegue; agrega segun sea necesario.
- Si existe un `calendar.db` en la raiz, se copia automaticamente a `data/calendar.db` al iniciar para conservar datos antiguos.
