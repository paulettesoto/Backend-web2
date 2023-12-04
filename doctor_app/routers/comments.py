from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header


router = APIRouter(
    prefix="/comments",
    tags=["Comentarios"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.get("/comments")
def getComments(idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("select * from comentarios where idDoctor=" + idDoctor + ";")
        cursor.execute(query)
        record = cursor.fetchall()
        # print(record)
        idcommentario, comentario, estrellas, iddoctor = record
        return {
            "id": idcommentario,
            "comentario": comentario,
            "estrellas": estrellas,
            "iddoctor": iddoctor
        }
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)