import os

from fasthtml.common import serve

from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    serve(port=port)
