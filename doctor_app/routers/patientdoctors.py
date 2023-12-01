from mysql.connector import Error
from ..connection import connection, cursor,connect
from fastapi import APIRouter

router = APIRouter(
    prefix="/patientdoctors",
    tags=["Doctores - paciente"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

@router.get("/buscar_doctor")
def buscar_doc(especialidad:str):
    connection()
    try:
        query="select * from doctor where Especialidad='"+especialidad+"';"
        cursor.execute(query)
        record = cursor.fetchall()
        if record is not None:
            return record
    except Error as e:
        return {"Error: ", e}