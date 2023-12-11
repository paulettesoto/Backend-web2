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
def dates(idDoctor: str, fecha:str):
    connect, cursor = connection()
    try:
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
            "WHERE c.Doctor_idDoctor = %s AND h.fecha = %s;"
        )
        values = (idDoctor, fecha)
        print(query)
        cursor.execute(query, values)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idcita, nombre,celular, dnombre, tratamiento, fecha, hora, confirm = record
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
#nomas
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
