from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
import enum

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://root:system@localhost/proyecto"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Enum para los tipos de lectura
class TipoLecturaEnum(enum.Enum):
    Entrada = "Entrada"
    Salida = "Salida"

# Modelos de la base de datos

class Persona(Base):
    __tablename__ = "persona"
    persona_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30))
    apellido = Column(String(30))
    dni = Column(String(20))
    grupo_id = Column(Integer, ForeignKey("grupo.grupo_id"))
    rol_id = Column(Integer, ForeignKey("rol.rol_id"))
    aula = Column(String(30))

class RegistroTarjeta(Base):
    __tablename__ = "registrotarjeta"
    id = Column(Integer, primary_key=True, index=True)
    tarjeta_id = Column(Integer, ForeignKey("tarjeta.id", ondelete="CASCADE"))
    fecha_lectura = Column(TIMESTAMP, default=datetime.utcnow)  # Fecha con valor por defecto
    tipo_lectura = Column(Enum(TipoLecturaEnum), default=TipoLecturaEnum.Entrada)  # Valor por defecto

# Modelos de Pydantic para la respuesta
class PersonaResponse(BaseModel):
    persona_id: int
    nombre: str
    apellido: str
    dni: str
    aula: str

    class Config:
        orm_mode = True

class RegistroTarjetaResponse(BaseModel):
    id: int
    tarjeta_id: int
    fecha_lectura: datetime
    tipo_lectura: TipoLecturaEnum

    class Config:
        orm_mode = True

# Inicialización de la API
app = FastAPI()

# Dependencia de la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/persones", response_model=list[PersonaResponse])
def get_persones(db: SessionLocal = Depends(get_db)):
    persones = db.query(Persona).all()
    return  

@app.get("/marcatges", response_model=list[RegistroTarjetaResponse])
def get_marcatges(db: SessionLocal = Depends(get_db)):
    marcatges = db.query(RegistroTarjeta).all()
    return marcatges

@app.get("/persones/{persona_id}", response_model=PersonaResponse)
def get_persona(persona_id: int, db: SessionLocal = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.persona_id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no trobada")
    return persona

@app.get("/marcatges/{id}", response_model=RegistroTarjetaResponse)
def get_marcatge(id: int, db: SessionLocal = Depends(get_db)):
    marcatge = db.query(RegistroTarjeta).filter(RegistroTarjeta.id == id).first()
    if not marcatge:
        raise HTTPException(status_code=404, detail="Marcatge no trobat")
    return marcatge

# Ejecuta el servidor: uvicorn main:app --reload
