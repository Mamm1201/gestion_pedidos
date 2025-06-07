# -----------------------------
#           MODELO BASE
# -----------------------------
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):  # Hereda desde BaseModel
    id: Optional[str] = None  # <-- Esto permite que 'id' sea omitido o nulo
    nombre: str
    email: str
    rol: str