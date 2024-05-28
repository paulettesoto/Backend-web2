from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header


router = APIRouter(
    prefix="/dates",
    tags=["Citas"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

def agregar_paciente(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, fecha_nac:str, Correo:str, edad:str,idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("insert into pacienteDoctor(Nombre,PrimerApe,SegundoApe,Celular,FechaNac,Correo,Edad,idDoctor,cuenta) values(%s,%s,%s,%s,%s,%s,%s,%s,0);")
        val =(Nombre,PrimerApe,SegundoApe,Celular,fecha_nac,Correo,edad,idDoctor)
        cursor.execute(query,val)
        connect.commit()
        last_inserted_id = str(cursor.lastrowid)
        return last_inserted_id
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

def ListaPacientes(idDoctor:str,celular:str):
    connect, cursor = connection()
    try:
        cursor.execute("select idPaciente from pacienteDoctor where Celular="+celular+" and idDoctor =" + idDoctor + ";")
        records = cursor.fetchone()


        if records:
            for record in records:
                id = record
            return id
        else:
            id=0
            return id
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
@router.post("/setDate")
def setDate(celular:str, correo:str, Nombre:str,PrimerApe:str,SegundoApe:str,idTratamiento:str,idDoctor:str,edad:str,fechanac:str, fecha:str, hora:str):
    if ListaPacientes(idDoctor,celular) == 0:
        idPaciente = agregar_paciente(Nombre,PrimerApe,SegundoApe,celular,fechanac,correo,edad,idDoctor)
    else:
        idPaciente = ListaPacientes(idDoctor,celular)

    connect, cursor = connection()
    try:
        query = ("select idhorarios from horarios where idDoctor=%s  and fecha=%s and hora =%s;")
        val = (idDoctor,fecha,hora)
        cursor.execute(query, val)
        record = cursor.fetchone()
        if record is not None:
            #return record
            # disconnection()
            # connection()
            try:
                id = str(record[0])
                query = ("insert into cita(Paciente_idPaciente,Doctor_idDoctor,idTratamiento,idHorario,account) "
                         "values(%s,%s,%s,%s,'N');")
                val = (idPaciente,idDoctor,idTratamiento,id)
                print(query, val)
                cursor.execute(query, val)
                connect.commit()
                # if record is not None:
                try:
                    query = ("update horarios set status=false where idhorarios=%s;")
                    val = (record)
                    cursor.execute(query, val)
                    connect.commit()
                    try:
                        query = ("INSERT INTO Status (tratamientos_idTratamiento, doctor_idDoctor, paciente_idPaciente, "
                                 "status, cuenta) VALUES (%s,%s,%s, b'0', b'0');")
                        val = (idTratamiento,idDoctor,idPaciente)
                        cursor.execute(query, val)
                        connect.commit()
                        return {"success": "agendado con exito"}
                    except Error as e:
                        return {"Error: ", e}
                    finally:
                        disconnection(connect, cursor)
                except Error as e:
                    return {"Error: ", e}
                finally:
                    disconnection(connect, cursor)
            except Error as e:
                return {"Error: ", e}
            finally:
                disconnection(connect, cursor)
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.delete("/cancelDate")
def canceldate(idCita:str):
    connect, cursor = connection()
    try:
        query = ("select idHorario from cita where idCIta=%s;")
        val = (idCita,)
        cursor.execute(query, val)
        record = cursor.fetchone()
        if record is not None:
            #return record
            # disconnection()
            # connection()
            try:
                query = ("delete from cita where idCita=%s;")
                val = (idCita,)
                cursor.execute(query, val)
                connect.commit()
                # if record is not None:
                try:
                    query = (
                        "UPDATE horarios SET status = TRUE, updated_at = NOW() "
                        "WHERE idhorarios = %s;"
                    )
                    val = (record)
                    cursor.execute(query, val)
                    connect.commit()
                    return {"success": "Cita cancelada con exito"}
                except Error as e:
                    return {"Error: ", e}
                finally:
                    disconnection(connect, cursor)
            except Error as e:
                return {"Error: ", e}
            finally:
                disconnection(connect, cursor)
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.get("/dates")
def dates(idDoctor: str, fecha:str):
    connect, cursor = connection()
    try:
        query = (
            "SELECT c.idCita, "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.idPaciente "
            "    WHEN c.account = 'Y' THEN p.idPaciente "  
            "END AS idPaciente, "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.Nombre "
            "    WHEN c.account = 'Y' THEN p.Nombre "  
            "END AS Nombre, "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.PrimerApe "
            "    WHEN c.account = 'Y' THEN p.PrimerApe "  
            "END AS PrimerApe, "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.Celular "
            "    WHEN c.account = 'Y' THEN p.Celular "  
            "END, "
            "d.Nombre AS NombreDoctor, "
            "t.Tratamiento, "
            "h.fecha, "
            "h.hora, "
            "c.confirmada "
            "FROM cita AS c "
            "LEFT JOIN paciente AS p ON p.idPaciente = c.Paciente_idPaciente "
            "LEFT JOIN pacienteDoctor AS pd ON pd.idPaciente = c.Paciente_idPaciente "
            "INNER JOIN doctor AS d ON d.idDoctor = c.Doctor_idDoctor "
            "INNER JOIN tratamientos AS t ON t.idTratamiento = c.idTratamiento "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s AND h.fecha = %s order by h.hora;"
        )
        values = (idDoctor, fecha)
        print(query)
        cursor.execute(query, values)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idcita,idPaciente, nombre, PrimerApe,celular, dnombre, tratamiento, fecha, hora, confirm = record
                date_dict = {
                    "id": idcita,
                    "idPaciente": idPaciente,
                    "PrimerApe": PrimerApe,
                    "Nombre": nombre,
                    "Celular": celular,
                    "Doctor": dnombre,
                    "tratamiento": tratamiento,
                    "fecha": fecha,
                    "hora": hora,
                    "confirmada": confirm
                }
                dates_list.append(date_dict)

            return {"dates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.get("/confirmAppointment")
def confirmApp(idCita:int):
    connect, cursor = connection()
    try:
        query = ("update cita set confirmada=1 where idCita=%s;")
        val = (idCita,)
        cursor.execute(query, val)
        connect.commit()
        # record = cursor.rowcount()
        # if record is not None:
        return {"success": "Cita confirmada con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

#reporte semanal
from datetime import datetime, timedelta


@router.get("/reportWeek")
def dates(idDoctor: str, fecha: str):
    connect, cursor = connection()
    try:
        # Convertir la fecha a un objeto datetime
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")

        # Calcular la fecha de inicio y fin de la semana
        inicio_semana = fecha_obj - timedelta(days=fecha_obj.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        query = (
            "SELECT c.idCita, "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.Nombre "
            "    WHEN c.account = 'Y' THEN p.Nombre "
            "END AS Nombre, "
            "CASE "
            "    WHEN c.account = 'N' THEN pd.Celular "
            "    WHEN c.account = 'Y' THEN p.Celular "
            "END, "
            "d.Nombre AS NombreDoctor, "
            "t.Tratamiento, "
            "h.fecha, "
            "h.hora, "
            "c.confirmada "
            "FROM cita AS c "
            "LEFT JOIN paciente AS p ON p.idPaciente = c.Paciente_idPaciente "
            "LEFT JOIN pacienteDoctor AS pd ON pd.idPaciente = c.Paciente_idPaciente "
            "INNER JOIN doctor AS d ON d.idDoctor = c.Doctor_idDoctor "
            "INNER JOIN tratamientos AS t ON t.idTratamiento = c.idTratamiento "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s AND h.fecha BETWEEN %s AND %s "
            "ORDER BY h.fecha;"
        )

        values = (idDoctor, inicio_semana.strftime("%Y-%m-%d"), fin_semana.strftime("%Y-%m-%d"))
        print(query)
        cursor.execute(query, values)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idcita, nombre, celular, dnombre, tratamiento, fecha, hora, confirm = record
                date_dict = {
                    "id": idcita,
                    "Nombre": nombre,
                    "Celular": celular,
                    "Doctor": dnombre,
                    "tratamiento": tratamiento,
                    "fecha": fecha,
                    "hora": hora,
                    "confirmada": confirm
                }
                dates_list.append(date_dict)

            return {"dates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

#reportmonth
@router.get("/reportMonth")
def dates(idDoctor: str):
    connect, cursor = connection()
    try:
        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Calcular el primer día del mes actual
        primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)

        query = (
            "SELECT c.idCita, "
            "COALESCE(pd.Nombre, p.Nombre) AS Nombre, "
            "COALESCE(pd.Celular, p.Celular) AS Celular, "
            "d.Nombre AS NombreDoctor, "
            "t.Tratamiento, "
            "h.fecha, "
            "h.hora, "
            "CASE "
            "    WHEN c.confirmada = 0 THEN 'No cumplida' "
            "    WHEN c.confirmada = 1 THEN 'Cumplida' "
            "    ELSE 'Pendiente' "
            "END AS confirmada "
            "FROM cita AS c "
            "LEFT JOIN paciente AS p ON p.idPaciente = c.Paciente_idPaciente "
            "LEFT JOIN pacienteDoctor AS pd ON pd.idPaciente = c.Paciente_idPaciente "
            "INNER JOIN doctor AS d ON d.idDoctor = c.Doctor_idDoctor "
            "INNER JOIN tratamientos AS t ON t.idTratamiento = c.idTratamiento "
            "INNER JOIN horarios AS h ON h.idhorarios = c.idHorario "
            "WHERE c.Doctor_idDoctor = %s "
            "AND h.fecha BETWEEN %s AND %s "
            "ORDER BY h.fecha;"
        )

        values = (idDoctor, primer_dia_mes.strftime("%Y-%m-%d"), fecha_actual.strftime("%Y-%m-%d"))
        print(query)
        cursor.execute(query, values)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idcita, nombre, celular, dnombre, tratamiento, fecha, hora, confirmada = record
                date_dict = {
                    "id": idcita,
                    "Nombre": nombre or '',  # Asegúrate de manejar NULL correctamente
                    "Celular": celular or '',  # Asegúrate de manejar NULL correctamente
                    "Doctor": dnombre or '',  # Asegúrate de manejar NULL correctamente
                    "tratamiento": tratamiento or '',  # Asegúrate de manejar NULL correctamente
                    "fecha": fecha.strftime("%Y-%m-%d") if fecha else '',  # Asegúrate de manejar NULL correctamente
                    "hora": hora or '',  # Asegúrate de manejar NULL correctamente
                    "confirmada": confirmada or ''  # Asegúrate de manejar NULL correctamente
                }
                dates_list.append(date_dict)

            return {"dates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)