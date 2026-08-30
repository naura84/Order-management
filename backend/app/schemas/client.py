from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class ClientCreate(BaseModel):
    nom: str
    email: EmailStr

class ClientUpdate(BaseModel):
    nom: str | None = None
    email: EmailStr | None = None     # Allow email and nom to be optional for updates


class ClientResponse(BaseModel):
    id: int
    nom: str
    email: EmailStr
    date_creation: datetime

    model_config = ConfigDict(from_attributes=True)