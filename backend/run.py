import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Permite redefinir host/puerto mediante variables de entorno sin editar código
    host = os.getenv("BACKEND_HOST", "127.0.0.1")
    port = int(os.getenv("BACKEND_PORT", os.getenv("PORT", 5001)))

    app.run(
        debug=app.config.get("DEBUG", True),
        host=host,
        port=port,
    )
