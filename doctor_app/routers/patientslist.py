from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header
#from..main import idDoctor

router = APIRouter(
    prefix="/patientslist",
    tags=["Lista pacientes"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("/listapacientes")
def ListaPacientes(idDoctor:str):
    connect, cursor = connection()
    try:
        cursor.execute("select * from paciente-doctor where idDoctor =" + idDoctor + ";")
        record = cursor.fetchall()
        if record is not None:
            idPaciente, nombre, primerApe,segundoApe, celular, fechaNac, correo,edad,iddoctor = record
            return {
                "id": idPaciente,
                "Nombre": nombre,
                "PrimerApe": primerApe,
                "SegundoApe": segundoApe,
                "celular": celular,
                "fechaNac": fechaNac,
                "correo": correo,
                "edad": edad,
                "idDoctor": iddoctor
            }
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.post("/agregar_paciente") #NO ES NECESARIA LA CONTRASEÑA CUANDO EL DOCTOR AGREGA UN PACIENTE
def agregar_paciente(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, fecha_nac:str, Correo:str, edad:str,idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("insert into paciente-doctor(Nombre,PrimerApe,SegundoApe,Celular,FechaNac,Correo,Edad,idDoctor) values(%s,%s,%s,%s,%s,%s,%s,%s);")
        val =(Nombre,PrimerApe,SegundoApe,Celular,fecha_nac,Correo,edad,idDoctor)
        cursor.execute(query,val)
        connect.commit()
        return {"success": "Registrado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.put("/update_paciente")
def update_paciente(idPaciente:int, Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str,fecha_nac:str, Correo:str,edad:str):
    connect, cursor = connection()
    try:
        query = ("update paciente set Nombre=%s, PrimerApe=%s, SegundoApe=%s, Celular=%s, FechaNac=%s, Correo=%s, Edad=%s where idPaciente=%s;")
        val =(Nombre,PrimerApe,SegundoApe,Celular,fecha_nac,Correo,edad,idPaciente)
        cursor.execute(query,val)
        connect.commit()
        return {"success": "Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.delete("/deletePaciente")
def deletePaciente(celular: str,idDoctor:str):
    connect, cursor = connection()
    try:
        query = "select idPaciente from paciente-doctor where idDoctor="+idDoctor+" and Celular="+celular+";"
        cursor.execute(query)
        record = cursor.fetchone()
        if record is not None:
            try:
                query = "delete from paciente-doctor where idPaciente=%s;"
                val = record
                print(record)
                cursor.execute(query, val)
                connect.commit()
                return {"success": "Eliminado con exito"}
            except Error as e:
                return {"Error: ", e}
            finally:
                disconnection(connect, cursor)
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
