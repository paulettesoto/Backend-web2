from mysql.connector import Error
from ..connection import connection, cursor,connect
from fastapi import APIRouter


router = APIRouter(
    prefix="/comments",
    tags=["Comentarios"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})

@router.post("/comentarios_paciente")
def comentarios_paciente(comentario:str,calificacion:int,idDoctor:int):
    connection()
    try:
        query = ("insert into comentarios(comentario, estrellas, idDoctor) values(%s,%s,%s);")
        val = (comentario,calificacion,idDoctor)
        cursor.execute(query, val)
        connect.commit()
        return {"Gracias por sus comentarios"}
    except Error as e:
        return {"Error: ", e}
