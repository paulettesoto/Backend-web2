from mysql.connector import Error
from ..connection import connection,disconnection,cursor,connect
from fastapi import APIRouter, Depends
from ..dependecies import get_token_header


router = APIRouter(
    prefix="/comments",
    tags=["Comentarios"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.get("/comments")
def getComments(idDoctor:str):
    connection()
    try:
        query = ("select * from comentarios where idDoctor=" + idDoctor + ";")
        cursor.execute(query)
        record = cursor.fetchall()
        # print(record)
        return record
    except Error as e:
        return {"Error: ", e}