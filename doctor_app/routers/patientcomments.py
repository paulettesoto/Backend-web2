from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter


router = APIRouter(
    prefix="/patientcomments",
    tags=["Comentarios paciente"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})

@router.post("/comentarios_paciente")
def comentarios_paciente(comentario:str,calificacion:int,idDoctor:int):
    connect, cursor = connection()
    try:
        query = ("insert into comentarios(comentario, estrellas, idDoctor) values(%s,%s,%s);")
        val = (comentario,calificacion,idDoctor)
        cursor.execute(query, val)
        connect.commit()
        return {"success": "Gracias por sus comentarios"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
