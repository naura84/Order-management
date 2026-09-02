import os

from fastapi import Header, HTTPException


API_KEY = os.getenv("API_KEY")


def verify_api_key(
    x_api_key: str | None = Header(default=None),
):
    if not API_KEY:
        raise RuntimeError("API_KEY is not configured.")

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Clé API invalide ou absente.",
        )

    return x_api_key