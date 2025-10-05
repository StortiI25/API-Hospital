from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    
class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class PacienteCreate(BaseModel):
    nome: str
    idade: int
    endereco: str | None = None

class PacienteOut(BaseModel):
    id: int
    nome: str
    idade: int
    endereco: str | None

    class Config:
        orm_mode = True

class MedicoCreate(BaseModel):
    nome: str
    especialidade: str

class MedicoOut(BaseModel):
    id: int
    nome: str
    especialidade: str

    class Config:
        orm_mode = True


