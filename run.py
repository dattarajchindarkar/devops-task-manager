import logging
import os
from app import create_app

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
