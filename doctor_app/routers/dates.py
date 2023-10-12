from mysql.connector import Error
from ..connection import connection,disconnection,cursor,connect
from fastapi import APIRouter, Depends
from ..dependecies import get_token_header


router = APIRouter(
    prefix="/dates",
    tags=["Citas"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.post("/setDate")
def setDate(idPaciente:str, idDoctor:str, idTratamiento:str, fecha:str, hora:str):
    connection()
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
                query = ("insert into cita(Paciente_idPaciente,Doctor_idDoctor,idTratamiento,idHorario) "
                         "values("+ idPaciente +","+ idDoctor +","+ idTratamiento +",%s);")
                val = (record)
                cursor.execute(query, val)
                connect.commit()
                # if record is not None:
                try:
                    query = ("update horarios set status=false where idhorarios=%s;")
                    val = (record)
                    cursor.execute(query, val)
                    connect.commit()
                    return {"agendado con exito"}
                except Error as e:
                    return {"Error: ", e}
            except Error as e:
                return {"Error: ", e}
    except Error as e:
        return {"Error: ", e}


@router.delete("/cancelDate")
def canceldate(idCita:str):
    connection()
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
                    return {"Cita cancelada con exito"}
                except Error as e:
                    return {"Error: ", e}
            except Error as e:
                return {"Error: ", e}
    except Error as e:
        return {"Error: ", e}


@router.get("/dates/")
def dates(idDoctor: str):
    connection()
    try:
        query = ("select c.idCita, p.Nombre, d.Nombre, t.Tratamiento, h.fecha,h.hora from cita as c "
                 "INNER JOIN paciente as p on p.idPaciente=c.Paciente_idPaciente INNER JOIN doctor as d "
                 "on d.idDoctor=c.Doctor_idDoctor INNER JOIN tratamientos as t on t.idTratamiento=c.idTratamiento "
                 "INNER JOIN horarios as h on h.idhorarios=c.idHorario where c.Doctor_idDoctor=" + idDoctor + ";")
        cursor.execute(query)
        record = cursor.fetchall()
        # print(record)
        return record
    except Error as e:
        return {"Error: ", e}
