import logging
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                "logs/app.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
    )