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
        last_inserted_id = cursor.lastrowid
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
        id = str(records[0])
        if records:
            return id
        else:
            return 0
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
@router.post("/setDate")
def setDate(celular:str, correo:str, Nombre:str,PrimerApe:str,SegundoApe:str,idTratamiento:str,idDoctor:str,edad:str,fechanac:str, fecha:str, hora:str, idPaciente:str):
    if ListaPacientes(idDoctor,celular) == 0:
        idPaciente = str(agregar_paciente(Nombre,PrimerApe,SegundoApe,celular,fechanac,correo,edad,idDoctor))
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
                val = str(record[0])
                query = ("insert into cita(Paciente_idPaciente,Doctor_idDoctor,idTratamiento,idHorario,account) "
                         "values("+ idPaciente +","+ idDoctor +","+ idTratamiento +","+val+",'N');")
                print(query)
                cursor.execute(query)
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
def dates(idDoctor: str, fecha:str):
    connect, cursor = connection()
    try:
        query = ("select c.idCita, p.Nombre, d.Nombre, t.Tratamiento, h.fecha,h.hora from cita as c "
                 "INNER JOIN paciente as p on p.idPaciente=c.Paciente_idPaciente INNER JOIN doctor as d "
                 "on d.idDoctor=c.Doctor_idDoctor INNER JOIN tratamientos as t on t.idTratamiento=c.idTratamiento "
                 "INNER JOIN horarios as h on h.idhorarios=c.idHorario where c.Doctor_idDoctor=" + idDoctor + " and h.fecha = "+fecha+" ;")
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            dates_list = []
            for record in records:
                idcita, nombre, dnombre, tratamiento, fecha, hora = record
                date_dict = {
                    "id": idcita,
                    "Nombre": nombre,
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
