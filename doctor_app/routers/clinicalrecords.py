from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/clinicalRecords",
    tags=["Historia Clinica"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("/clinicalRecords")
def getQuestions(idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("select * from historiaclinica where idDoctor=" + idDoctor + ";")
        cursor.execute(query)
        record = cursor.fetchall()
        # print(record)
        return record
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.post("/addQuestion")
def addQuestion(pregunta:str,idDoctor:str):
    connect, cursor = connection()
    try:
        query = ("insert into historiaclinica(Pregunta,idDoctor) values(%s,%s);")
        val =(pregunta,idDoctor)
        cursor.execute(query,val)
        connect.commit()
        return {"Registrado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.put("/updateQuestion")
def updateQuestion(idHistoriaClinica:str, pregunta:str):
    connect, cursor = connection()
    try:
        query = ("update historiaclinica set pregunta=%s where idhistoriaClinica=%s;")
        val =(pregunta,idHistoriaClinica)
        cursor.execute(query,val)
        connect.commit()
        return {"Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.delete("/deleteQuestion")
def deleteQuestion(idHistoriaClinica: str):
    connect, cursor = connection()
    try:

        query = "delete from historiaclinica where idhistoriaClinica="+idHistoriaClinica+";"
        #val = idHistoriaClinica
        cursor.execute(query)
        connect.commit()
        return {"Eliminado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)



