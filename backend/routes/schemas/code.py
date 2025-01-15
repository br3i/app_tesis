from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# Definir los posibles valores para el estado del código
class CodeStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    used = "used"
    unused = "unused"

class CodeBase(BaseModel):
    code: str
    status: CodeStatus = CodeStatus.active
    created_at: datetime
    expires_at: datetime
    used_at: datetime | None = None

    class Config:
        from_attributes = True  # Permite que FastAPI convierta objetos SQLAlchemy a Pydantic

class CodeCreate(CodeBase):
    pass

class CodeResponse(CodeBase):
    id: int
