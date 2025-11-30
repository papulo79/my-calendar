# Vision general
- Aplicacion de calendario mensual hecha con FastHTML (Starlette + HTMX + fastlite). Solo hay un modulo principal `main.py`, assets estaticos en `assets/` y la base SQLite `calendar.db`.
- Dependencias de runtime: Python 3.10+, paquete `fasthtml` (incluye fastlite/uvicorn/htmx). Emoji picker llega por CDN (`emoji-picker-element`), sin bundling extra. No hay `requirements.txt`.
- `serve()` al final de `main.py` levanta el server en el puerto 5001; `fast_app(live=True)` habilita autoreload.

# Datos y modelos
- DB SQLite `calendar.db`; tablas creadas en arranque si faltan:
  - `categories`: `id` (pk int), `name`, `icon`, `color`.
  - `events`: `id` (pk int), `category_id` (FK a categories), `date` (YYYY-MM-DD), `note`.
- fastlite expone tablas como `db.t.categories`/`db.t.events`; se crean dataclasses `Category` y `Event` via `.dataclass()`.
- Para limpiar datos basta borrar `calendar.db` (no hay migraciones).

# Rutas y flujo HTMX
- `/`: vista principal; acepta `year`, `month`, `lang`, `filter_cat_id` (GET). Renderiza calendario mensual con filtros por categoria, selector de idioma, toggle de tema y control de navegacion.
- `/categories` GET: gestiona categorias (form emoji + nombre + color). Incluye toggle de tema/idioma y boton de volver.
- `/categories` POST: inserta categoria y redirige a `/categories`.
- `/categories/{id}` DELETE: borra categoria, retorna vacio.
- `/day/{date}` GET: devuelve modal HTMX con eventos del dia y formulario para agregar.
- `/events` POST: inserta evento; devuelve item para la lista del modal + `DayCell` re-renderizado con `hx-swap-oob`. Nota: `DayCell` aqui se renderiza con idioma `"es"` fijo.
- `/events/{id}` DELETE: borra evento y devuelve `DayCell` actualizado con `hx-swap-oob` (idioma tambien fijo en `"es"`).
- `/assets/{fname:path}`: sirve `assets/styles.css` y `assets/scripts.js`.

# UI y comportamiento
- Componentes clave en `main.py`: `CategoryBadge`, `LangSelector` (usa `Select` con redireccion por query `?lang=`), `ThemeToggle` (llama a `toggleTheme()` en JS), `DayCell` (calculado por semana/dia; marca hoy; muestra eventos con icono y color de categoria).
- Traducciones en `TRANSLATIONS`; `get_lang(sess)` lee `lang` desde la sesion y por defecto usa `'es'`. Header incluye selector de idioma y el valor se persiste en sesion via query `lang`.
- JS (`assets/scripts.js`): `openDayModal`/`closeDayModal` via HTMX, emoji picker toggle/click, persistencia de tema en `localStorage`, Escape cierra modal/picker, `toggleTheme` alterna `data-theme`.
- CSS (`assets/styles.css`): variables para light/dark, layout responsive (mobile colapsa calendario en lista), estilos para modales, pills de eventos, selector de idioma y botones.

# Puntos a vigilar / futuras mejoras
- Localizacion de OOB swaps: los handlers de `/events` usan idioma fijo `"es"` para re-renderizar `DayCell`; si se quiere respetar idioma de sesion hay que inyectar `session`/`lang` en esos handlers o guardar el idioma en el evento.
- No hay validacion de colisiones de fechas ni control de limites de categorias/eventos.
- Sin pruebas automatizadas; si agregas tests usa `starlette.testclient`/`fasthtml` helpers.
- Sin configuracion de despliegue; depende de `serve()` por ahora.

# Referencias rapidas
- Ejecutar: `python main.py` y abre `http://localhost:5001`.
- El contexto de FastHTML completo esta en `context/llms-ctx-full.txt` (guia de API y ejemplos).
