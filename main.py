from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, Usuario, Medico
from passlib.hash import bcrypt
from schemas import UsuarioCreate, UsuarioLogin, MedicoCreate, MedicoOut
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if db_usuario is None:
        raise credentials_exception
    return db_usuario  

@app.post("/cadastro/")
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    usuario.senha = bcrypt.hash(usuario.senha)
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/login/")
def login_usuario(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not db_usuario or not bcrypt.verify(usuario.senha, db_usuario.senha):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_usuario.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/medico", response_model=MedicoOut)
def create_medico(medico: MedicoCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_atual)):
    db_medico = db.query(Medico).filter(Medico.nome == medico.nome).first()
    if db_medico:
        raise HTTPException(status_code=400, detail="Médico já registrado")
    db_medico = Medico(nome=medico.nome, especialidade=medico.especialidade)
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

@app.post("/medico",response_model=list[MedicoOut])
def get_medico(db: Session = Depends(get_db), usuario: Usuario = Depends()):
    medicos = db.query(Medico).all()
    return medicos


