import os

from fasthtml.common import serve

from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    host = os.environ.get("HOST", "0.0.0.0")
    serve(host=host, port=port)
