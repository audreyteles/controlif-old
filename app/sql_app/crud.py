import ast
import json

import redis
from sqlalchemy.orm import Session
from . import models
from sqlalchemy import select, Table, MetaData, text

r = redis.Redis(host='redis', port=6379, decode_responses=True)


def get_activities(db: Session):
    return db.query(models.Atividade).all()


def get_view(db: Session):
    result = db.execute(
        text(
            """
        SELECT
   a.idAtividades AS idAtividades,
   a.nome AS nome_atividade,
   pa.Atividades_idAtividades AS Atividades_idAtividades,
   pa.Participantes_idParticipantes AS Participantes_idParticipantes,
   DATE_FORMAT(pa.entrada, '%Y-%m-%d %H:%i:%s') AS entrada,
   DATE_FORMAT(pa.saida, '%Y-%m-%d %H:%i:%s') AS saida,
   p.idParticipantes AS idParticipantes,
   p.nome AS nome_participante,
   p.email AS email
FROM
   snct.atividades a
   JOIN snct.participantes_tem_atividades pa ON a.idAtividades = pa.Atividades_idAtividades
   JOIN snct.participantes p ON pa.Participantes_idParticipantes = p.idParticipantes;

           """))

    return result.fetchall()


def set_presences(db: Session):
    return db.query(models.Participante).all()


def set_presence(db: Session, data):
    """
    {"atividade":"1","participante":"7","entrada":true,"saida":true}
    """
    data = ast.literal_eval(data)

    if data['saida'] == 1:
        result = db.execute(
            text(
                f""" 
                UPDATE snct.participantes_tem_atividades SET participantes_tem_atividades.saida=now()
                WHERE Participantes_idParticipantes={data["participante"]} AND Atividades_idAtividades={data['atividade']};
                """))
        db.commit()
        print("aqui")
    else:
        result = db.execute(
            text(
                f""" 
                       UPDATE snct.participantes_tem_atividades SET participantes_tem_atividades.entrada=now()
                       WHERE Participantes_idParticipantes={data["participante"]} AND Atividades_idAtividades={data['atividade']};
                       """))
        db.commit()
    data = get_view(db)
    data = ast.literal_eval(str(data))
    dados_json = [
        {
            "id_atividade": tupla[0],
            "nome_atividade": tupla[1],
            "id_participacao": tupla[2],
            "entrada": tupla[4],
            "saída": tupla[5],
            "id_participante": tupla[6],

            # Adicione outros campos conforme necessário
            "nome_participante": tupla[7],
            "email_participante": tupla[8]
        }
        for tupla in data
    ]
    dados_json_str = json.dumps(dados_json)
    r.set('allData', dados_json_str)

    return result
