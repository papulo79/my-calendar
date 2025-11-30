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
        "mon": "Mon",
        "tue": "Tue",
        "wed": "Wed",
        "thu": "Thu",
        "fri": "Fri",
        "sat": "Sat",
        "sun": "Sun",
        "january": "January",
        "february": "February",
        "march": "March",
        "april": "April",
        "may": "May",
        "june": "June",
        "july": "July",
        "august": "August",
        "september": "September",
        "october": "October",
        "november": "November",
        "december": "December",
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
        "mon": "Lun",
        "tue": "Mar",
        "wed": "Mié",
        "thu": "Jue",
        "fri": "Vie",
        "sat": "Sáb",
        "sun": "Dom",
        "january": "Enero",
        "february": "Febrero",
        "march": "Marzo",
        "april": "Abril",
        "may": "Mayo",
        "june": "Junio",
        "july": "Julio",
        "august": "Agosto",
        "september": "Septiembre",
        "october": "Octubre",
        "november": "Noviembre",
        "december": "Diciembre",
    },
}


def t(key, lang="en"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)


def get_lang(session):
    return session.get("lang", "es")


def get_month_name(month, lang="en"):
    months = [
        "",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    return t(months[month], lang)


__all__ = ["t", "get_lang", "get_month_name", "TRANSLATIONS"]
