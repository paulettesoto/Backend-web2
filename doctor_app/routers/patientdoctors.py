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