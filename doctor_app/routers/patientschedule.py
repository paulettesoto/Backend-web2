from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/doctorschedules",
    tags=["Horarios"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.get("/availableDates")
def availableDates(idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("select * from horarios where idDoctor="+idDoctor+" and status=true;")
        #print(query)
        #val = (idDoctor)
        cursor.execute(query)
        record = cursor.fetchall()
        #print(record)
        idHorario, idDoctor, fecha, hora, status = record
        return {
            "id": idHorario,
            "Nombre": idDoctor,
            "PrimerApe": fecha,
            "SegundoApe": hora,
            "status": status
        }
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)