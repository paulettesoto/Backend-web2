from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

router = APIRouter(
    prefix="/patientdoctors",
    tags=["Doctores - paciente"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

@router.get("/buscar_doctor")
def buscar_doc(especialidad:str):
    connect, cursor = connection()
    try:
        query="select idDoctor, Nombre, PrimerApe, SegundoApe, Celular, Especialidad, Correo, Cedula, Foto from doctor where Especialidad='"+especialidad+"';"
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            doctors_list = []
            for record in records:
                iddoctor, nombre, primer_ape, segundo_ape, celular, especialidad, correo, cedula, foto = record
                doctor_dict = {
                    "id": iddoctor,
                    "Nombre": nombre,
                    "PrimerApe": primer_ape,
                    "SegundoApe": segundo_ape,
                    "Celular": celular,
                    "Especialidad": especialidad,
                    "Correo": correo,
                    "Cedula": cedula,
                    "Foto": foto
                }
                doctors_list.append(doctor_dict)
            return {"doctors": doctors_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.get("/favorites")
def favorites(idPaciente: str):
    connect, cursor = connection()
    try:
        query = ("select DISTINCT  c.Doctor_idDoctor, d.Nombre, d.PrimerApe, d.SegundoApe, d.Especialidad, d.Cedula, "
                 "d.Celular, d.Foto from cita as c "
                 "INNER JOIN doctor as d on d.idDoctor=c.Doctor_idDoctor "
                 "where c.Paciente_idPaciente=" + idPaciente + " and account='Y';")
        cursor.execute(query)
        records = cursor.fetchall()

        if records:
            favorites_list = []
            for record in records:
                idDoctor, nombre, apellido1, apellido2, especialidad, cedula, celular = record
                favorites_dict = {
                    "id": idDoctor,
                    "Nombre": nombre,
                    "PrimerApe": apellido1,
                    "SegundoApe": apellido2,
                    "especialidad": especialidad,
                    "cedula": cedula,
                    "celular": celular
                }
                favorites_list.append(favorites_dict)

            return {"favorites": favorites_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
