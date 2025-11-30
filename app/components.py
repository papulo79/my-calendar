import calendar
from datetime import datetime

from fasthtml.common import Button, Div, Option, Select, Span

from .i18n import t


def CategoryBadge(cat):
    return Span(
        f"{cat.icon} {cat.name}",
        cls="category-badge",
        style=f"background-color: {cat.color}20; color: {cat.color}; border: 1px solid {cat.color}40;",
    )


def LangSelector(curr_lang):
    return Select(
        Option("🇺🇸 English", value="en", selected=(curr_lang == "en")),
        Option("🇪🇸 Español", value="es", selected=(curr_lang == "es")),
        onchange="window.location.href='?lang='+this.value",
        cls="input-select lang-select",
    )


def ThemeToggle():
    return Button("🌓", onclick="toggleTheme()", cls="theme-toggle-btn", title="Toggle Theme")


def DayCell(day, month, year, day_events, categories_map, lang="es"):
    if day == 0:
        return Div(cls="day-cell empty")

    date_str = f"{year}-{month:02d}-{day:02d}"
    is_today = date_str == datetime.now().strftime("%Y-%m-%d")

    wd = calendar.weekday(year, month, day)
    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    wd_label = t(weekdays[wd], lang)

    todays_events = [e for e in day_events if e.date == date_str]

    def render_event(ev):
        cat = categories_map.get(ev.category_id)
        if not cat:
            return None
        return Div(
            cat.icon,
            Span(ev.note, cls="event-pill-note") if ev.note else "",
            cls="event-dot",
            style=f"background-color: {cat.color}40; color: {cat.color}",
            title=f"{cat.name}: {ev.note}",
        )

    return Div(
        Div(wd_label, cls="mobile-weekday-label"),
        Div(str(day), cls=f"day-number {'today' if is_today else ''}"),
        Div(*(e for e in (render_event(ev) for ev in todays_events) if e), cls="day-events"),
        cls=f"day-cell {'week-start' if wd == 0 else ''}",
        id=f"day-{date_str}",
        onclick=f"openDayModal('{date_str}')",
    )


__all__ = ["CategoryBadge", "LangSelector", "ThemeToggle", "DayCell"]
