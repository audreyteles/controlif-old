import ast
import json
from typing import List
import cv2
import numpy as np
import redis
from fastapi import APIRouter, status, UploadFile, File, Depends, Form
from modules.students import processing_image
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import datetime

from sql_app import crud
from sql_app.main import get_db
from sql_app import schemas

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}},
)

r = redis.Redis(host='redis', port=6379, decode_responses=True)


@router.post("/", status_code=status.HTTP_200_OK,
             summary="Retorna as informações do aluno com base na foto")
async def read_student(file: UploadFile = File(...), activity: str = Form(...)):
    print(activity)
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return_student = processing_image(frame, activity)

    return {
        "name": return_student['name_partcipant'],
        "data": return_student['data']
    }


@router.post("/all", status_code=status.HTTP_200_OK,
             summary="Retorna as atividades e dados")
async def read_all(db: Session = Depends(get_db)):
    if r.get("allData"):
        data = r.get("allData")
        data = json.loads(data)
        return JSONResponse(content=data)
    else:
        data = crud.get_view(db)
        data = ast.literal_eval(str(data))
        print(data)
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
        return dados_json


@router.post("/activities", status_code=status.HTTP_200_OK, response_model=schemas.Atividade,
             summary="Retorna as atividades")
async def read_activities(db: Session = Depends(get_db)):
    data = crud.get_activities(db)
    result = jsonable_encoder(data)
    return JSONResponse(content=result)


@router.post("/validations", status_code=status.HTTP_200_OK,
             summary="Valida a atividade do participante")
async def set_validation(db: Session = Depends(get_db), data: str = Form(...)):
    result = crud.set_presence(db, data)
    return result
