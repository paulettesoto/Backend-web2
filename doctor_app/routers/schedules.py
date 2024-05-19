from mysql.connector import Error
from ..connection import connection,disconnection
from fastapi import APIRouter
from datetime import timedelta, datetime

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/schedules",
    tags=["Horarios"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.post("/addDates")
def addDates(idDoctor:int, fecha_inicio:str,fecha_final:str, hora_inicio:str,hora_final:str,status:bool):
    connect, cursor = connection()
    try:
        start_date = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        end_date = datetime.strptime(fecha_final, "%Y-%m-%d")
        start_time = datetime.strptime(hora_inicio, "%H:%M").time()
        end_time = datetime.strptime(hora_final, "%H:%M").time()

        current_date = start_date
        appointments = []

        while current_date <= end_date:
            current_time = datetime.combine(current_date, start_time)
            end_time_on_current_day = datetime.combine(current_date, end_time)

            while current_time <= end_time_on_current_day:
                appointments.append((
                    idDoctor,
                    current_time.strftime("%Y-%m-%d"),
                    current_time.strftime("%H:%M:%S"),
                    status,
                    current_time.strftime("%Y-%m-%d"),
                    current_time.strftime("%H:%M:%S")
                ))
                current_time += timedelta(minutes=30)  # Asumimos que cada cita dura 30 minutos

            current_date += timedelta(days=1)

        query = ("INSERT INTO horarios (idDoctor, fecha, hora, status) "
                 "SELECT %s, %s, %s, %s FROM dual "
                 "WHERE NOT EXISTS (SELECT 1 FROM horarios WHERE fecha = %s AND hora = %s);")

        for appointment in appointments:
            cursor.execute(query, appointment)

        connect.commit()
        return {"success": "Insertado con éxito"}
    except Error as e:
        return {"error": str(e)}
    finally:
        disconnection(connect, cursor)


@router.get("/availableDates")
def availableDates(idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("select * from horarios where idDoctor="+idDoctor+" and status=true and fecha>=CURRENT_DATE() order by fecha,idhorarios;")
        print(query)
        #val = (idDoctor)
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            dates_list = {}
            for record in records:
                idHorario, idDoctor, fecha, hora, status = record
                date_entry = {
                    "id": idHorario,
                    "idDoctor": idDoctor,
                    "hora": hora,
                    "status": status
                }
                if fecha not in dates_list:
                    dates_list[fecha] = []

                dates_list[fecha].append(date_entry)
            return {"availableDates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.delete("/deleteDates")
def deleteDates(idHorario:str):
    connect, cursor = connection()
    try:
        query = ("delete from horarios where idhorarios=%s;")
        val = (idHorario,)
        cursor.execute(query, val)
        connect.commit()
        # record = cursor.rowcount()
        # if record is not None:
        return {"success": "Eliminado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


