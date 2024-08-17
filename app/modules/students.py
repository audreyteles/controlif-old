import json

import cv2 as cv
import redis
from deepface import DeepFace
from pyjarowinkler import distance
import ast

r = redis.Redis(host='redis', port=6379, decode_responses=True)


def processing_image(frame, value):
    # face_objs = DeepFace.extract_faces(img_path=frame, enforce_detection=False)

    face_objs = DeepFace.extract_faces(
        img_path=frame,
        enforce_detection=False,
        grayscale=True,
        align=True,
        detector_backend="ssd"

    )
    left = face_objs[0]['facial_area']['x']
    top = face_objs[0]['facial_area']['y']
    w = face_objs[0]['facial_area']['w']
    h = face_objs[0]['facial_area']['h']
    bottom = (h + top)
    rigth = left + w
    data = None

    try:
        result = DeepFace.find(img_path=frame,
                               db_path="database",
                               enforce_detection=True,
                               model_name="Facenet",
                               detector_backend="retinaface",
                               align=True,
                               )
        if result[0].empty or result[0]['Facenet_cosine'][0] >= 0.299:
            print(result[0].to_markdown())
            name = "Desconhecido"
        else:
            print(result[0].to_markdown())

            name = f"{result[0]['identity'].iloc[0]}"

            name = name.split("\\")
            name = name[1].split("/")[0]

            name = name.replace("_", " ")
            name = name.replace(".PNG", "")

            if r.get("allData"):
                result = []
                data = []

                for idx, item in enumerate(json.loads(r.get("allData"))):
                    print(item)
                    if int(item['id_atividade']) == int(value):
                        print(result)
                        result.append(
                            distance.get_jaro_distance(item['nome_participante'], name, winkler=True, scaling=0.1))
                        data.append(
                            (item, distance.get_jaro_distance(item['nome_participante'], name, winkler=True, scaling=0.1)))

                result = max(result)

                if result >= 0.80:
                    for test in data:
                        if test[1] == result:
                            name = test[0]['email_participante']
                            data = test[0]
                else:
                    name = "Não inscrito nessa atividade!"

    except:
        name = "Nenhum rosto identificado!"
    return {
        "name_partcipant": name,
        "data": data,
    }
