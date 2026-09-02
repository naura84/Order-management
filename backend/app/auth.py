import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()


def verify_api_key(x_api_key: str | None = Header(default=None)):
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise RuntimeError("API_KEY is not configured.")

    if x_api_key != api_key:
        raise HTTPException(
            status_code=401,
            detail="Clé API invalide ou absente."
        )