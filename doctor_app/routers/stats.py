from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter
from datetime import datetime, timedelta
import calendar


router = APIRouter(
    prefix="/stats",
    tags=["Estadisticas"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("/calificacion")
def getCalificacion(idDoctor: str):
    connect, cursor = connection()
    try:
        query = "SELECT estrellas FROM comentarios WHERE idDoctor = %s;"
        cursor.execute(query, (idDoctor,))
        records = cursor.fetchall()

        if records:
            estrellas_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

            for record in records:
                estrellas = record[0]
                if estrellas in estrellas_count:
                    estrellas_count[estrellas] += 1

            comments_list = [{k : v} for k, v in estrellas_count.items()]

            return {"comments": comments_list}
        else:
            return {"comments": []}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)


@router.get("/treatments")
def treatments(idDoctor: str, year: str, month: str):
    connect, cursor = connection()
    try:
        query = (
            "SELECT t.Tratamiento, COUNT(*) AS cantidad "
            "FROM cita AS c "
            "INNER JOIN tratamientos AS t ON t.idTratamiento = c.idTratamiento "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s AND YEAR(h.fecha) = %s AND MONTH(h.fecha) = %s "
            "GROUP BY t.Tratamiento;"
        )
        values = (idDoctor, year, month)
        cursor.execute(query, values)
        records = cursor.fetchall()

        if records:
            treatments_list = []
            for record in records:
                tratamiento, cantidad = record
                treatment_dict = {
                    "tratamiento": tratamiento,
                    "cantidad": cantidad
                }
                treatments_list.append(treatment_dict)

            return {"treatments": treatments_list}
        else:
            return {"treatments": []}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)


@router.get("/attendance")
def attendance(idDoctor: str, year: str, month: str):
    connect, cursor = connection()
    try:
        # Generar todos los días del mes
        _, last_day = calendar.monthrange(int(year), int(month))
        all_days = [datetime(int(year), int(month), day).strftime("%Y-%m-%d") for day in range(1, last_day + 1)]
        query = (
            "SELECT DATE(h.fecha) AS fecha, COUNT(*) AS cantidad "
            "FROM cita AS c "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s AND YEAR(h.fecha) = %s AND MONTH(h.fecha) = %s AND c.confirmada = '1' "
            "GROUP BY DATE(h.fecha);"
        )
        values = (idDoctor, year, month)
        cursor.execute(query, values)
        records = cursor.fetchall()

        if records:
            confirmed_dates = {record[0].strftime("%Y-%m-%d"): record[1] for record in records}

            dates_list = []
            for day in all_days:
                dates_list.append({
                    "fecha": day,
                    "cantidad": confirmed_dates.get(day, 0)
                })

            return {"dates": dates_list}
        else:
            return {"dates": []}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)


@router.get("/ages")
def ages(idDoctor: str, year: str, month: str):
    connect, cursor = connection()
    try:

        query = (
            "SELECT "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.FechaNac "
            "    WHEN c.account = 'Y' THEN p.FechaNac "
            "END AS edad "
            "FROM cita AS c "
            "LEFT JOIN paciente AS p ON p.idPaciente = c.Paciente_idPaciente "
            "LEFT JOIN pacienteDoctor AS pd ON pd.idPaciente = c.Paciente_idPaciente "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s AND YEAR(h.fecha) = %s AND MONTH(h.fecha) = %s AND c.confirmada = 1;"
        )
        values = (idDoctor, year, month)
        cursor.execute(query, values)
        records = cursor.fetchall()

        # Diccionario para contar los pacientes por rangos de edad
        age_ranges = {
            "0-9": 0,
            "10-19": 0,
            "20-29": 0,
            "30-39": 0,
            "40-49": 0,
            "50-59": 0,
            "60-69": 0,
            "70-79": 0,
            "80-89": 0,
            "90-99": 0,
            "100+": 0,
        }

        current_date = datetime.now()

        if records:
            for record in records:
                fechaNacimiento = record[0]
                if fechaNacimiento:
                    birth_date = datetime.strptime(str(fechaNacimiento), "%Y-%m-%d")
                    age = current_date.year - birth_date.year - (
                                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
                    if age < 10:
                        age_ranges["0-9"] += 1
                    elif age < 20:
                        age_ranges["10-19"] += 1
                    elif age < 30:
                        age_ranges["20-29"] += 1
                    elif age < 40:
                        age_ranges["30-39"] += 1
                    elif age < 50:
                        age_ranges["40-49"] += 1
                    elif age < 60:
                        age_ranges["50-59"] += 1
                    elif age < 70:
                        age_ranges["60-69"] += 1
                    elif age < 80:
                        age_ranges["70-79"] += 1
                    elif age < 90:
                        age_ranges["80-89"] += 1
                    elif age < 100:
                        age_ranges["90-99"] += 1
                    else:
                        age_ranges["100+"] += 1

            return {"age_ranges": age_ranges}
        else:
            return {"age_ranges": age_ranges}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)


@router.get("/used_dates")
def dates(idDoctor: str):
    connect, cursor = connection()
    try:
        # Consulta SQL para obtener las citas del doctor en el mes especificado y su estado
        query = (
            "SELECT "
            "SUM(CASE WHEN status = FALSE THEN 1 ELSE 0 END) AS ocupadas, "
            "SUM(CASE WHEN status = TRUE THEN 1 ELSE 0 END) AS no_ocupadas "
            "FROM horarios "
            "WHERE idDoctor = %s;"
        )
        values = (idDoctor,)
        cursor.execute(query, values)
        records = cursor.fetchall()

        dates_list = {}
        if records:
            for record in records:
                ocupadas, no_ocupadas = record
                dates_list = {
                    "ocupadas": ocupadas,
                    "no_ocupadas": no_ocupadas
                }

            return {"used_dates": dates_list}
        else:
            return {"used_dates": {}}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)

def format_timedelta_to_hhmm(timedelta_obj):
    total_seconds = int(timedelta_obj.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"
@router.get("/used_hours")
def get_used_hours(idDoctor: str):
    connect, cursor = connection()
    try:
        query = (
            "SELECT hora, COUNT(*) AS ocupadas "
            "FROM horarios "
            "WHERE idDoctor = %s AND status = 0 "
            "GROUP BY hora;"
        )
        values = (idDoctor,)
        cursor.execute(query, values)
        records = cursor.fetchall()

        hours_dict = {}
        if records:
            for record in records:
                hora, ocupadas = record
                formatted_hour = format_timedelta_to_hhmm(hora)
                hours_dict[formatted_hour] = ocupadas

        return {"used_hours": hours_dict}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)


@router.get("/canceladas-atendidas")
def canceladasatendidas(idDoctor: str, year: str, month: str):
    connect, cursor = connection()
    try:
        _, last_day = calendar.monthrange(int(year), int(month))
        all_days = [datetime(int(year), int(month), day).strftime("%Y-%m-%d") for day in range(1, last_day + 1)]

        query_confirmed = (
            "SELECT h.fecha, COUNT(*) AS cantidad "
            "FROM cita AS c "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s AND YEAR(h.fecha) = %s AND MONTH(h.fecha) = %s AND c.confirmada = '1' "
            "GROUP BY h.fecha;"
        )
        values = (idDoctor, year, month)
        cursor.execute(query_confirmed, values)
        confirmed_records = cursor.fetchall()
        print(confirmed_records)

        query_cancelled = (
            "SELECT fecha, COUNT(*) AS cantidad "
            "FROM horarios "
            "WHERE idDoctor = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s AND updated_at IS NOT NULL "
            "GROUP BY fecha;"
        )
        cursor.execute(query_cancelled, values)
        cancelled_records = cursor.fetchall()
        print(cancelled_records)

        confirmed_dates = {record[0].strftime("%Y-%m-%d"): record[1] for record in confirmed_records}
        cancelled_dates = {record[0].strftime("%Y-%m-%d"): record[1] for record in cancelled_records}

        dates_list = []
        for day in all_days:
            dates_list.append({
                "fecha": day,
                "confirmadas": confirmed_dates.get(day, 0),
                "canceladas": cancelled_dates.get(day, 0)
            })

        return {"dates": dates_list}
    except Error as e:
        return {"Error": str(e)}
    finally:
        disconnection(connect, cursor)