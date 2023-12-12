from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

router = APIRouter(
    prefix="/patientdates",
    tags=["Citas paciente"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.post("/setDate")
def setDate(idPaciente:str, idDoctor:str, idTratamiento:str, fecha:str, hora:str):
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
                query = ("insert into cita(Paciente_idPaciente,Doctor_idDoctor,idTratamiento,idHorario,account) "
                         "values("+ idPaciente +","+ idDoctor +","+ idTratamiento +",%s, 'Y');")
                val = (record)
                cursor.execute(query, val)
                connect.commit()
                # if record is not None:
                try:
                    query = ("update horarios set status=false where idhorarios=%s;")
                    val = (record)
                    cursor.execute(query, val)
                    connect.commit()
                    try:
                        query = ("INSERT INTO Status (tratamientos_idTratamiento, doctor_idDoctor, paciente_idPaciente, status, cuenta) VALUES (%s,%s,%s, b'0', b'1');")
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
        val = (idCita)
        cursor.execute(query, val)
        record = cursor.fetchone()
        if record is not None:
            #return record
            # disconnection()
            # connection()
            try:
                query = ("delete from cita where idCita=%s;")
                val = (idCita)
                cursor.execute(query, val)
                connect.commit()
                # if record is not None:
                try:
                    query = ("update horarios set status=true where idhorarios=%s;")
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
def dates(idPaciente: str):
    connect, cursor = connection()
    try:
        query = ("select c.idCita, p.Nombre, d.idDoctor, d.Nombre, t.Tratamiento, h.fecha,h.hora from cita as c "
                 "INNER JOIN paciente as p on p.idPaciente=c.Paciente_idPaciente INNER JOIN doctor as d "
                 "on d.idDoctor=c.Doctor_idDoctor INNER JOIN tratamientos as t on t.idTratamiento=c.idTratamiento "
                 "INNER JOIN horarios as h on h.idhorarios=c.idHorario where c.Paciente_idPaciente=" + idPaciente + " and account='Y';")
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idcita, nombre, idDoc, dnombre, tratamiento, fecha, hora = record
                date_dict = {
                    "id": idcita,
                    "Nombre": nombre,
                    "idDoctor": idDoc,
                    "Doctor": dnombre,
                    "tratamiento": tratamiento,
                    "fecha": fecha,
                    "hora": hora
                }
                dates_list.append(date_dict)

            return {"dates": dates_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
