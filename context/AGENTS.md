# Vision general
- Aplicacion de calendario mensual hecha con FastHTML (Starlette + HTMX + fastlite). Estructura modular en `app/` (rutas, componentes, i18n, db) con assets estaticos en `assets/` y la base SQLite en `data/calendar.db`.
- Dependencias de runtime: Python 3.10+, paquete `fasthtml` (incluye fastlite/uvicorn/htmx). Emoji picker llega por CDN (`emoji-picker-element`), sin bundling extra. No hay `requirements.txt`.
- `serve()` en `main.py` levanta el server (puerto configurable via `PORT`, por defecto 5001); `fast_app(live=True)` habilita autoreload.

# Datos y modelos
- DB SQLite `data/calendar.db`; tablas creadas en arranque si faltan:
  - `categories`: `id` (pk int), `name`, `icon`, `color`.
  - `events`: `id` (pk int), `category_id` (FK a categories), `date` (YYYY-MM-DD), `note`.
- fastlite expone tablas como `db.t.categories`/`db.t.events`; se crean dataclasses `Category` y `Event` via `.dataclass()`.
- Para limpiar datos basta borrar `data/calendar.db` (no hay migraciones). Si existe `calendar.db` en la raiz, se copia automaticamente a `data/`.

# Rutas y flujo HTMX
- `/`: vista principal; acepta `year`, `month`, `lang`, `filter_cat_id` (GET). Renderiza calendario mensual con filtros por categoria, selector de idioma, toggle de tema y control de navegacion.
- `/categories` GET: gestiona categorias (form emoji + nombre + color). Incluye toggle de tema/idioma y boton de volver.
- `/categories` POST: inserta categoria y redirige a `/categories`.
- `/categories/{id}` DELETE: borra categoria, retorna vacio.
- `/day/{date}` GET: devuelve modal HTMX con eventos del dia y formulario para agregar.
- `/events` POST: inserta evento; devuelve item para la lista del modal + `DayCell` re-renderizado con `hx-swap-oob` (respeta idioma de sesion).
- `/events/{id}` DELETE: borra evento y devuelve `DayCell` actualizado con `hx-swap-oob` (respeta idioma de sesion).
- `/assets/{fname:path}`: sirve `assets/styles.css` y `assets/scripts.js`.
- Favicon en `assets/favicon.svg` enlazado en headers.

- Componentes clave en `app/components.py`: `CategoryBadge`, `LangSelector` (usa `Select` con redireccion por query `?lang=`), `ThemeToggle` (llama a `toggleTheme()` en JS), `DayCell` (calculado por semana/dia; marca hoy; muestra eventos con icono y color de categoria).
- Traducciones en `TRANSLATIONS`; `get_lang(sess)` lee `lang` desde la sesion y por defecto usa `'es'`. Header incluye selector de idioma y el valor se persiste en sesion via query `lang`.
- JS (`assets/scripts.js`): `openDayModal`/`closeDayModal` via HTMX, emoji picker toggle/click, persistencia de tema en `localStorage`, Escape cierra modal/picker, `toggleTheme` alterna `data-theme`, `toggleOptionsPanel` muestra/oculta panel de idioma/tema en movil.
- CSS (`assets/styles.css`): variables para light/dark, layout responsive (mobile colapsa calendario en lista), cabecera responsive (desktop en una linea, movil con boton “⋮” a la derecha y panel de opciones bajo el titulo), estilos para modales, pills de eventos, selector de idioma y botones.

# Puntos a vigilar / futuras mejoras
- Localizacion de OOB swaps: ya se respeta el idioma de sesion en los handlers de `/events`; mantener esta firma si se expanden rutas.
- No hay validacion de colisiones de fechas ni control de limites de categorias/eventos.
- Sin pruebas automatizadas; si agregas tests usa `starlette.testclient`/`fasthtml` helpers.
- Sin configuracion de despliegue; depende de `serve()` por ahora.

# Referencias rapidas
- Ejecutar: `python main.py` y abre `http://localhost:5001`.
- El contexto de FastHTML completo esta en `context/llms-ctx-full.txt` (guia de API y ejemplos).
