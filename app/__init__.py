from fasthtml.common import Link, Script, fast_app

from .routes import register_routes


def build_headers():
    return (
        Link(rel="stylesheet", href="/assets/styles.css"),
        Link(rel="preconnect", href="https://fonts.googleapis.com"),
        Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        Script(src="https://cdn.jsdelivr.net/npm/emoji-picker-element@^1/index.js", type="module"),
        Script(src="/assets/scripts.js"),
    )


# Build the app and register all routes up-front
app, rt = fast_app(hdrs=build_headers(), live=True)
register_routes(app, rt)

__all__ = ["app"]
