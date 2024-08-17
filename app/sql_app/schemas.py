from typing import TypeVar, Optional
from pydantic import BaseModel
from pydantic.schema import datetime

T = TypeVar('T')


class Student(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Aluno da Silva",
            }
        }


class ParticipanteCreate(BaseModel):
    nome: str
    email: str


class Participante(BaseModel):
    idParticipantes: int
    nome: str
    email: str


class AtividadeCreate(BaseModel):
    nome: str


class Atividade(BaseModel):
    idAtividades: int
    nome: str
    descricao: str


class ParticipanteAtividadeCreate(BaseModel):
    Participantes_idParticipantes: int
    Atividades_idAtividades: int
    entrada: datetime | None = None
    saida: datetime | None = None


class ViewAtividadesComParticipantes(BaseModel):
    idAtividades: int
    nome_atividade: str
    Atividades_idAtividades: int
    Participantes_idParticipantes: int
    entrada: Optional[datetime]
    saida: Optional[datetime]
    idParticipantes: int
    nome_participante: str
    email: str

    class Config:
        orm_mode = True
