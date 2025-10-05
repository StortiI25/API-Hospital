from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATADASE_URL = "sqlite:///./hospital.db"

engine = create_engine(DATADASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha = Column(String)

    medicos = relationship("Medico", back_populates="usuario", uselist=False)
    pacientes = relationship("Paciente", back_populates="usuario", uselist=False)


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    endereco = Column(String)

    usuario = relationship("Usuario", back_populates="pacientes")

class Medico(Base):
    __tablename__ = "medicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="medicos")

