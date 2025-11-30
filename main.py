from fasthtml.common import *
from datetime import datetime, timedelta
import calendar
import locale

# Translations
TRANSLATIONS = {
    "en": {
        "title": "Calendar",
        "my_calendar": "My Calendar",
        "categories": "Categories",
        "manage_categories": "Manage Categories",
        "back": "← Back",
        "add_category": "Add Category",
        "category_name": "Category Name",
        "icon": "Icon",
        "events_for": "Events for",
        "add_event": "Add Event",
        "add_note": "Add a note...",
        "filter_by": "Filter by Category",
        "all_categories": "All Categories",
        "color": "Color",
        "mon": "Mon", "tue": "Tue", "wed": "Wed", "thu": "Thu", "fri": "Fri", "sat": "Sat", "sun": "Sun",
        "january": "January", "february": "February", "march": "March", "april": "April", "may": "May", "june": "June",
        "july": "July", "august": "August", "september": "September", "october": "October", "november": "November", "december": "December"
    },
    "es": {
        "title": "Calendario",
        "my_calendar": "Mi Calendario",
        "categories": "Categorías",
        "manage_categories": "Gestionar Categorías",
        "back": "← Volver",
        "add_category": "Añadir Categoría",
        "category_name": "Nombre de la Categoría",
        "icon": "Icono",
        "events_for": "Eventos para",
        "add_event": "Añadir Evento",
        "add_note": "Añadir nota...",
        "filter_by": "Filtrar por Categoría",
        "all_categories": "Todas las Categorías",
        "color": "Color",
        "mon": "Lun", "tue": "Mar", "wed": "Mié", "thu": "Jue", "fri": "Vie", "sat": "Sáb", "sun": "Dom",
        "january": "Enero", "february": "Febrero", "march": "Marzo", "april": "Abril", "may": "Mayo", "june": "Junio",
        "july": "Julio", "august": "Agosto", "september": "Septiembre", "october": "Octubre", "november": "Noviembre", "december": "Diciembre"
    }
}

def t(key, lang="en"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def get_lang(session):
    return session.get('lang', 'es') # Default to ES as requested implicitly by user language

app, rt = fast_app(
    hdrs=(
        Link(rel='stylesheet', href='/assets/styles.css'),
        Link(rel="preconnect", href="https://fonts.googleapis.com"),
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap", rel="stylesheet"),
        Script(src="https://cdn.jsdelivr.net/npm/emoji-picker-element@^1/index.js", type="module"),
        Script(src="/assets/scripts.js"),
    ),
    live=True
)

# Database Setup
db = database('calendar.db')
categories = db.t.categories
events = db.t.events

if categories not in db.t:
    categories.create(
        id=int, 
        name=str, 
        icon=str, 
        color=str, 
        pk='id'
    )
if events not in db.t:
    events.create(
        id=int, 
        category_id=int, 
        date=str, 
        note=str, 
        pk='id',
        foreign_keys=[('category_id', 'categories')]
    )

Category = categories.dataclass()
Event = events.dataclass()

# Helpers
def get_month_calendar(year, month):
    cal = calendar.Calendar()
    return cal.monthdayscalendar(year, month)

def get_month_name(month, lang="en"):
    # Use our translation dict for months to ensure consistency
    months_en = ["", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    return t(months_en[month], lang)

# Components
def CategoryBadge(cat):
    return Span(
        f"{cat.icon} {cat.name}",
        cls="category-badge",
        style=f"background-color: {cat.color}20; color: {cat.color}; border: 1px solid {cat.color}40;"
    )

def LangSelector(curr_lang):
    return Select(
        Option("🇺🇸 English", value="en", selected=(curr_lang == "en")),
        Option("🇪🇸 Español", value="es", selected=(curr_lang == "es")),
        onchange="window.location.href='?lang='+this.value",
        cls="input-select lang-select"
    )

def ThemeToggle():
    return Button(
        "🌓",
        onclick="toggleTheme()",
        cls="theme-toggle-btn",
        title="Toggle Theme"
    )

def DayCell(day, month, year, day_events, lang="es"):
    if day == 0:
        return Div(cls="day-cell empty")
    
    date_str = f"{year}-{month:02d}-{day:02d}"
    is_today = date_str == datetime.now().strftime("%Y-%m-%d")
    
    # Calculate weekday
    wd = calendar.weekday(year, month, day)
    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    wd_label = t(weekdays[wd], lang)
    
    # Filter events for this day
    todays_events = [e for e in day_events if e.date == date_str]
    
    return Div(
        Div(wd_label, cls="mobile-weekday-label"),
        Div(str(day), cls=f"day-number {'today' if is_today else ''}"),
        Div(
            *[
                Div(
                    categories[e.category_id].icon,
                    Span(e.note, cls="event-pill-note") if e.note else "",
                    cls="event-dot",
                    style=f"background-color: {categories[e.category_id].color}40; color: {categories[e.category_id].color}",
                    title=f"{categories[e.category_id].name}: {e.note}"
                ) for e in todays_events
            ],
            cls="day-events"
        ),
        cls=f"day-cell {'week-start' if wd == 0 else ''}",
        id=f"day-{date_str}",
        onclick=f"openDayModal('{date_str}')"
    )

# Routes
@rt("/")
def get(session, year: int = None, month: int = None, lang: str = None, filter_cat_id: int = None):
    if lang: session['lang'] = lang
    curr_lang = get_lang(session)
    
    now = datetime.now()
    if not year: year = now.year
    if not month: month = now.month
    
    # Navigation logic
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    cal_weeks = get_month_calendar(year, month)
    
    # Fetch events
    all_events = events()
    if filter_cat_id and filter_cat_id > 0:
        all_events = [e for e in all_events if e.category_id == filter_cat_id]
        
    cats = categories()
    
    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    
    return Title(t("title", curr_lang)), Main(
        # 1. Title, Theme, Lang
        Div(
            H1(t("my_calendar", curr_lang), cls="app-title"),
            Div(
                ThemeToggle(),
                LangSelector(curr_lang),
                cls="header-controls-top"
            ),
            cls="header-top"
        ),
        # 2. Categories & Filter
        Div(
            Form(
                Select(
                    Option(t("all_categories", curr_lang), value="0"),
                    *[Option(f"{c.icon} {c.name}", value=c.id, selected=(c.id == filter_cat_id)) for c in cats],
                    name="filter_cat_id",
                    onchange="this.form.submit()",
                    cls="input-select filter-select"
                ),
                method="get",
                cls="filter-form"
            ),
            A(t("categories", curr_lang), href="/categories", cls="btn secondary"),
            cls="header-controls-middle"
        ),
        # 3. Month Navigation
        Div(
            A("←", href=f"/?year={prev_year}&month={prev_month}", cls="nav-btn"),
            H2(f"{get_month_name(month, curr_lang)} {year}", cls="month-title"),
            A("→", href=f"/?year={next_year}&month={next_month}", cls="nav-btn"),
            cls="calendar-nav-controls centered-nav"
        ),
        Div(
            *[Div(t(d, curr_lang), cls="weekday-header") for d in weekdays],
            cls="calendar-grid-header"
        ),
        Div(
            *[
                DayCell(day, month, year, all_events, curr_lang) 
                for week in cal_weeks 
                for day in week
            ],
            cls="calendar-grid"
        ),
        # Modal Placeholder (Hidden by default)
        Div(id="day-modal-container"),
        cls="container"
    )

@rt("/categories")
def get(session, lang: str = None):
    if lang: session['lang'] = lang
    curr_lang = get_lang(session)
    
    cats = categories()
    return Title(t("categories", curr_lang)), Main(
        Div(
            H1(t("manage_categories", curr_lang), cls="app-title"),
            Div(
                ThemeToggle(),
                LangSelector(curr_lang),
                A(t("back", curr_lang), href="/", cls="btn secondary"),
                cls="header-actions"
            ),
            cls="header"
        ),
        Form(
            Div(
                Div(
                    Input(name="icon", id="icon-input", placeholder=t("icon", curr_lang), required=True, maxlength=2, cls="input-icon", readonly=True, onclick="toggleEmojiPicker()"),
                    Div(
                        NotStr("<emoji-picker></emoji-picker>"),
                        id="emoji-picker-container",
                        cls="emoji-picker-popover hidden"
                    ),
                    cls="icon-picker-wrapper"
                ),
                Input(name="name", placeholder=t("category_name", curr_lang), required=True, cls="input-text flex-grow"),
                Div(
                    Label(t("color", curr_lang), cls="input-label"),
                    Input(type="color", name="color", value="#3b82f6", cls="input-color"),
                    cls="color-picker-wrapper"
                ),
                cls="form-row"
            ),
            Div(
                Button(t("add_category", curr_lang), cls="btn primary"),
                cls="form-actions centered"
            ),
            action="/categories", method="post",
            cls="category-form"
        ),
        Div(
            *[
                Div(
                    CategoryBadge(c),
                    Button("✕", hx_delete=f"/categories/{c.id}", hx_target="closest .category-item", cls="btn-icon delete"),
                    cls="category-item"
                ) for c in cats
            ],
            cls="category-list"
        ),
        cls="container"
    )

@rt("/categories", methods=["POST"])
def post(cat: Category):
    categories.insert(cat)
    return RedirectResponse("/categories", status_code=303)

@rt("/categories/{id}", methods=["DELETE"])
def delete(id: int):
    categories.delete(id)
    return ""

# Day Modal Logic
@rt("/day/{date}")
def get(session, date: str):
    curr_lang = get_lang(session)
    # Fetch events for this day
    day_events = [e for e in events() if e.date == date]
    cats = categories()
    
    return Div(
        Div(
            Div(
                H3(f"{t('events_for', curr_lang)} {date}", cls="modal-title"),
                Button("✕", onclick="closeDayModal()", cls="btn-icon close"),
                cls="modal-header"
            ),
            Div(
                *[
                    Div(
                        CategoryBadge(categories[e.category_id]),
                        Span(e.note, cls="event-note"),
                        Button("✕", hx_delete=f"/events/{e.id}", hx_target="closest .event-item", cls="btn-icon delete-small"),
                        cls="event-item"
                    ) for e in day_events
                ],
                id="day-events-list",
                cls="day-events-list"
            ),
            Form(
                Select(
                    *[Option(f"{c.icon} {c.name}", value=c.id) for c in cats],
                    name="category_id",
                    required=True,
                    cls="input-select"
                ),
                Input(name="note", placeholder=t("add_note", curr_lang), cls="input-text"),
                Input(type="hidden", name="date", value=date),
                Button(t("add_event", curr_lang), cls="btn primary full-width"),
                hx_post="/events",
                hx_target="#day-events-list",
                hx_swap="beforeend",
                cls="event-form"
            ),
            cls="modal-content"
        ),
        cls="modal-backdrop",
        id="day-modal",
        onclick="if(event.target === this) closeDayModal()"
    )

@rt("/events", methods=["POST"])
def post(ev: Event):
    new_id = events.insert(ev)
    cat = categories[ev.category_id]
    
    # 1. Return the new event item for the modal list
    new_event_item = Div(
        CategoryBadge(cat),
        Span(ev.note, cls="event-note"),
        Button("✕", hx_delete=f"/events/{new_id}", hx_target="closest .event-item", cls="btn-icon delete-small"),
        cls="event-item"
    )
    
    # 2. Return OOB swap to update the day cell in the calendar grid
    # We need to re-render the DayCell for this date
    date_parts = ev.date.split('-')
    year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
    
    # Fetch all events for this day to re-render the cell correctly
    day_events = [e for e in events() if e.date == ev.date]
    
    # We need lang for DayCell, but we don't have session here easily without changing signature
    # For now, default to 'es' or try to get it if possible. 
    # Better: Update post signature to accept session
    updated_day_cell = DayCell(day, month, year, day_events, "es") # Defaulting to ES for OOB updates for now
    # Mark it for OOB swap
    updated_day_cell.attrs['hx-swap-oob'] = 'true'
    
    return new_event_item, updated_day_cell

@rt("/events/{id}", methods=["DELETE"])
def delete(id: int):
    # Get event before deleting to know which day to update
    ev = events[id]
    events.delete(id)
    
    # Return OOB swap to update the day cell
    date_parts = ev.date.split('-')
    year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
    day_events = [e for e in events() if e.date == ev.date]
    
    updated_day_cell = DayCell(day, month, year, day_events, "es")
    updated_day_cell.attrs['hx-swap-oob'] = 'true'
    
    return updated_day_cell

# Serve static assets
@rt("/assets/{fname:path}")
def get(fname: str): return FileResponse(f"assets/{fname}")

serve()
