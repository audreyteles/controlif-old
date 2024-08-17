from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base


class Atividade(Base):
    __tablename__ = 'atividades'

    idAtividades = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)

    # participantes_view = relationship('ViewAtividadesComParticipantes', back_populates='atividade')


class Participante(Base):
    __tablename__ = 'participantes'

    idParticipantes = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)


class ParticipanteAtividade(Base):
    __tablename__ = 'participantes_tem_atividades'

    idParticipantesTemAtividades = Column(Integer, primary_key=True)
    Participantes_idParticipantes = Column(Integer, ForeignKey('participantes.idParticipantes'))
    Atividades_idAtividades = Column(Integer, ForeignKey('atividades.idAtividades'))
    entrada = Column(DateTime)
    saida = Column(DateTime)


class ViewAtividadesComParticipantes(Base):
    __tablename__ = 'view_atividades_com_participantes'
    #id = Column(Integer, primary_key=True, autoincrement=True)

    idAtividades = Column(Integer, primary_key=True)
    nome_atividade = Column(String)
    Atividades_idAtividades = Column(Integer, ForeignKey('atividades.idAtividades'))
    Participantes_idParticipantes = Column(Integer, ForeignKey('participantes.idParticipantes'))
    entrada = Column(DateTime)
    saida = Column(DateTime)
    idParticipantes = Column(Integer)
    nome_participante = Column(String)
    email = Column(String)
