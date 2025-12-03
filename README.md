# My Calendar (FastHTML)

Calendario mensual con HTMX/FastHTML y SQLite, pensado para gestionar categorias con emoji y eventos rapidos desde modales.

## Caracteristicas
- **Multiusuario**: Sistema de autenticación para 3 usuarios (Pablo, Eva, Fer), cada uno con sus categorías y eventos privados.
- Vista mensual con navegacion de meses y resaltado del dia actual.
- Filtro por categoria y pagina dedicada para crear/eliminar categorias (emoji + color).
- Modal por dia para listar, agregar y borrar eventos sin recargar.
- Selector de idioma (en/es) y cambio de tema claro/oscuro persistido en `localStorage`.
- Datos persistentes en `data/calendar.db` (SQLite) manejados via fastlite.

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

`data/calendar.db` se crea automáticamente si no existe. Para reiniciar datos, borra el archivo.

> **⚠️ IMPORTANTE**: Los datos NO se sincronizan con Git (están en `.gitignore`). Ver `DEPLOYMENT.md` para gestión de datos en producción.

> Nota: `fasthtml` se instala desde GitHub (no esta en PyPI), por eso el `requirements.txt` usa una URL git.

## Uso rapido
- Vista principal (`/`): navegar meses, filtrar por categoria, cambiar idioma/tema. Click en un dia abre modal para eventos.
- Modal de dia: selecciona categoria, agrega nota opcional y envia; HTMX actualiza la lista y el calendario con `hx-swap-oob`.
- Categorias (`/categories`): crea nuevas categorias (emoji picker + color) o elimina existentes. Boton "Volver" regresa al calendario.

## Estructura del proyecto
- `main.py`: punto de entrada, solo arranca `serve()` usando la app modular.
- `app/`: logica principal separada.
  - `__init__.py`: construye `fast_app` con headers, beforeware de autenticación y registra rutas.
  - `auth.py`: gestión de usuarios (Pablo, Eva, Fer) y autenticación básica.
  - `routes.py`: controladores HTMX (login, home, categorias, modales de dias, CRUD de eventos) y assets estaticos. La cabecera se adapta: en desktop va en una sola linea (titulo | filtro + boton categorias | controles tema/idioma) y en movil muestra un boton "⋮" que despliega tema/idioma debajo del titulo.
  - `components.py`: componentes UI (`DayCell`, `LangSelector`, `ThemeToggle`, etc.).
  - `i18n.py`: traducciones y helpers de idioma/mes.
  - `db.py`: inicializa fastlite, crea tablas con campo `owner` para multiusuario y expone dataclasses `Category` y `Event` (usa `data/calendar.db`).
- `assets/styles.css`: tema light/dark, layout del calendario, modales y controles; layout responsivo de cabecera (desktop linea unica, movil con boton de opciones y panel desplegable).
- `assets/scripts.js`: manejo de modal HTMX, emoji picker, toggles de tema e idioma, boton de opciones en movil, atajos de teclado (Escape).
- `data/`: directorio para la base de datos (creado automáticamente).
  - `calendar.db`: base de datos SQLite con tablas `categories` y `events` (se autogenera con columna `owner`).
  - `backups/`: respaldos automáticos de la BD (excluido de git).
- `backup_db.sh` / `restore_db.sh`: scripts para gestión de respaldos de la base de datos.
- `context/llms-ctx*.txt`: referencia de FastHTML incluida para el entorno de IA.
- `DEPLOYMENT.md`: guía completa de despliegue en producción y gestión de datos.

## Notas de implementacion
- **Autenticación**: Sistema de beforeware que redirige a `/login` si no hay usuario en sesión. Las contraseñas se configuran via variables de entorno (`PABLO_PASSWORD`, `EVA_PASSWORD`, `FER_PASSWORD`).
- **Multiusuario**: Cada usuario tiene sus propios datos (categorías y eventos) filtrados por el campo `owner` en las tablas.
- El idioma se guarda en sesion (`lang`), por defecto `'es'`; los swaps OOB de eventos usan el idioma activo de la sesion.
- Los assets se sirven via `/assets/{fname:path}`; no hay pipeline de build.
- No hay pruebas automatizadas.

## Gestión de respaldos
```bash
# Crear respaldo manual
./backup_db.sh

# Restaurar desde un respaldo
./restore_db.sh calendar_YYYYMMDD_HHMMSS.db

# Listar respaldos disponibles
ls -lh data/backups/
```

Los scripts mantienen automáticamente solo los últimos 10 respaldos.
