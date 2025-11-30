import calendar
from datetime import datetime

from fasthtml.common import A, Button, Div, FileResponse, Form, H1, H2, H3, Hidden, Input, Main, NotStr, Option, RedirectResponse, Select, Span, Title

from .components import CategoryBadge, DayCell, LangSelector, ThemeToggle
from .db import Category, Event, categories, events
from .i18n import get_lang, get_month_name, t


def get_month_calendar(year, month):
    return calendar.Calendar().monthdayscalendar(year, month)


def build_daycell_for_date(date_str, categories_map, lang):
    year, month, day = map(int, date_str.split("-"))
    day_events = [e for e in events() if e.date == date_str]
    cell = DayCell(day, month, year, day_events, categories_map, lang)
    cell.attrs["hx-swap-oob"] = "true"
    return cell


def register_routes(app, rt):
    @rt("/", methods=["GET"])
    def home(session, year: int = None, month: int = None, lang: str = None, filter_cat_id: int = None):
        if lang:
            session["lang"] = lang
        curr_lang = get_lang(session)

        now = datetime.now()
        if not year:
            year = now.year
        if not month:
            month = now.month

        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        cal_weeks = get_month_calendar(year, month)

        all_events = events()
        if filter_cat_id and filter_cat_id > 0:
            all_events = [e for e in all_events if e.category_id == filter_cat_id]

        cats = categories()
        cats_by_id = {c.id: c for c in cats}
        weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

        return Title(t("title", curr_lang)), Main(
            Div(
                H1(t("my_calendar", curr_lang), cls="app-title"),
                Div(ThemeToggle(), LangSelector(curr_lang), cls="header-controls-top"),
                cls="header-top",
            ),
            Div(
                Form(
                    Hidden(name="lang", value=curr_lang),
                    Hidden(name="year", value=year),
                    Hidden(name="month", value=month),
                    Select(
                        Option(t("all_categories", curr_lang), value="0"),
                        *[
                            Option(f"{c.icon} {c.name}", value=c.id, selected=(c.id == filter_cat_id))
                            for c in cats
                        ],
                        name="filter_cat_id",
                        onchange="this.form.submit()",
                        cls="input-select filter-select",
                    ),
                    method="get",
                    cls="filter-form",
                ),
                A(t("categories", curr_lang), href="/categories", cls="btn secondary"),
                cls="header-controls-middle",
            ),
            Div(
                A("←", href=f"/?year={prev_year}&month={prev_month}", cls="nav-btn"),
                H2(f"{get_month_name(month, curr_lang)} {year}", cls="month-title"),
                A("→", href=f"/?year={next_year}&month={next_month}", cls="nav-btn"),
                cls="calendar-nav-controls centered-nav",
            ),
            Div(*(Div(t(d, curr_lang), cls="weekday-header") for d in weekdays), cls="calendar-grid-header"),
            Div(
                *(
                    DayCell(day, month, year, all_events, cats_by_id, curr_lang)
                    for week in cal_weeks
                    for day in week
                ),
                cls="calendar-grid",
            ),
            Div(id="day-modal-container"),
            cls="container",
        )

    @rt("/categories", methods=["GET"])
    def categories_page(session, lang: str = None):
        if lang:
            session["lang"] = lang
        curr_lang = get_lang(session)

        cats = categories()
        return Title(t("categories", curr_lang)), Main(
            Div(
                H1(t("manage_categories", curr_lang), cls="app-title"),
                Div(ThemeToggle(), LangSelector(curr_lang), A(t("back", curr_lang), href="/", cls="btn secondary"), cls="header-actions"),
                cls="header",
            ),
            Form(
                Div(
                    Div(
                        Span(t("icon", curr_lang), cls="input-label"),
                        Div(
                            Input(
                                name="icon",
                                id="icon-input",
                                placeholder=t("icon", curr_lang),
                                required=True,
                                maxlength=2,
                                cls="input-icon",
                                readonly=True,
                                onclick="toggleEmojiPicker()",
                            ),
                            Div(
                                NotStr("<emoji-picker></emoji-picker>"),
                                id="emoji-picker-container",
                                cls="emoji-picker-popover hidden",
                            ),
                            cls="icon-picker-wrapper",
                        ),
                        cls="form-field",
                    ),
                    Div(
                        Span(t("category_name", curr_lang), cls="input-label"),
                        Input(name="name", placeholder=t("category_name", curr_lang), required=True, cls="input-text"),
                        cls="form-field",
                    ),
                    Div(
                        Span(t("color", curr_lang), cls="input-label"),
                        Input(type="color", name="color", value="#3b82f6", cls="input-color"),
                        cls="form-field color-picker-wrapper",
                    ),
                    cls="form-grid",
                ),
                Div(Button(t("add_category", curr_lang), cls="btn primary"), cls="form-actions centered"),
                action="/categories",
                method="post",
                cls="category-form",
            ),
            Div(
                *(
                    Div(
                        CategoryBadge(c),
                        Button(
                            "✕",
                            hx_delete=f"/categories/{c.id}",
                            hx_target="closest .category-item",
                            hx_swap="outerHTML",
                            cls="btn-icon delete",
                        ),
                        cls="category-item",
                    )
                    for c in cats
                ),
                cls="category-list",
            ),
            cls="container",
        )

    @rt("/categories", methods=["POST"])
    def create_category(name: str, icon: str, color: str):
        categories.insert(dict(name=name, icon=icon, color=color))
        return RedirectResponse("/categories", status_code=303)

    @rt("/categories/{id}", methods=["DELETE"])
    def delete_category(id: int):
        categories.delete(id)
        return ""

    @rt("/day/{date}")
    def day_modal(session, date: str):
        curr_lang = get_lang(session)
        day_events = [e for e in events() if e.date == date]
        cats_by_id = {c.id: c for c in categories()}

        return Div(
            Div(
                Div(
                    H3(f"{t('events_for', curr_lang)} {date}", cls="modal-title"),
                    Button("✕", onclick="closeDayModal()", cls="btn-icon close"),
                    cls="modal-header",
                ),
                Div(
                    *(
                        Div(
                            CategoryBadge(cats_by_id[e.category_id]),
                            Span(e.note, cls="event-note"),
                            Button("✕", hx_delete=f"/events/{e.id}", hx_target="closest .event-item", cls="btn-icon delete-small"),
                            cls="event-item",
                        )
                        for e in day_events
                        if e.category_id in cats_by_id
                    ),
                    id="day-events-list",
                    cls="day-events-list",
                ),
                Form(
                    Select(
                        *(Option(f"{c.icon} {c.name}", value=c.id) for c in cats_by_id.values()),
                        name="category_id",
                        required=True,
                        cls="input-select",
                    ),
                    Input(name="note", placeholder=t("add_note", curr_lang), cls="input-text"),
                    Input(type="hidden", name="date", value=date),
                    Button(t("add_event", curr_lang), cls="btn primary full-width"),
                    hx_post="/events",
                    hx_target="#day-events-list",
                    hx_swap="beforeend",
                    cls="event-form",
                ),
                cls="modal-content",
            ),
            cls="modal-backdrop",
            id="day-modal",
            onclick="if(event.target === this) closeDayModal()",
        )

    @rt("/events", methods=["POST"])
    def create_event(ev: Event, session):
        new_id = events.insert(ev)
        cats_by_id = {c.id: c for c in categories()}
        cat = cats_by_id.get(ev.category_id)

        new_event_item = Div(
            CategoryBadge(cat),
            Span(ev.note, cls="event-note"),
            Button("✕", hx_delete=f"/events/{new_id}", hx_target="closest .event-item", cls="btn-icon delete-small"),
            cls="event-item",
        ) if cat else ""

        lang = get_lang(session)
        updated_day_cell = build_daycell_for_date(ev.date, cats_by_id, lang)

        return new_event_item, updated_day_cell

    @rt("/events/{id}", methods=["DELETE"])
    def delete_event(id: int, session):
        ev = events[id]
        events.delete(id)
        cats_by_id = {c.id: c for c in categories()}
        lang = get_lang(session)
        updated_day_cell = build_daycell_for_date(ev.date, cats_by_id, lang)
        return updated_day_cell

    @rt("/assets/{fname:path}")
    def assets(fname: str):
        return FileResponse(f"assets/{fname}")

    return app


__all__ = ["register_routes"]
