from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.code import Code
from models.database import get_db  # Suponiendo que tienes esta función para obtener la sesión de la DB
from routes.schemas.code import CodeCreate, CodeResponse
from datetime import datetime

router = APIRouter()

# Modelo de consulta para la entrada de datos
class CodeCreateRequest(BaseModel):
    code: str
    expires_at: datetime
    status: str = "active"

# Ruta para crear un código
@router.post("/create_code", response_model=CodeResponse)
async def create_code(data: CodeCreateRequest, db: Session = Depends(get_db)):
    new_code = Code(
        code=data.code,
        status=data.status,
        expires_at=data.expires_at
    )
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code

# Ruta para obtener un código por ID
@router.get("/get_code/{code_id}", response_model=CodeResponse)
async def get_code(code_id: int, db: Session = Depends(get_db)):
    code = db.query(Code).filter(Code.id == code_id).first()
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return code
