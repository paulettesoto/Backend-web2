from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/patientschedules",
    tags=["Horarios paciente"],
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
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idHorario, idDoctor, fecha, hora, status = record
                date_dict = {
                    "id": idHorario,
                    "idDoctor": idDoctor,
                    "fecha": fecha,
                    "hora": hora,
                    "status": status
                }
                dates_list.append(date_dict)

            return {"availableDates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)