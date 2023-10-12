from mysql.connector import Error
from ..connection import connection, cursor,connect
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/treatments",
    tags=["Tratamientos"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("/treatments")
def getTreatments(idDoctor:str):
    connection()
    try:
        query = ("select * from tratamientos where idDoctor=" + idDoctor + ";")
        cursor.execute(query)
        record = cursor.fetchall()
        # print(record)
        return record
    except Error as e:
        return {"Error: ", e}


@router.post("/addTreatment")
def addtreatment(tratamiento:str,idDoctor:str,costo:str):
    connection()
    try:
        query = ("insert into tratamientos(Tratamiento,idDoctor,Costo) values(%s,%s,%s);")
        val =(tratamiento,idDoctor,costo)
        cursor.execute(query,val)
        connect.commit()
        return {"Registrado con exito"}
    except Error as e:
        return {"Error: ", e}

@router.put("/updateTreatment")
def updateTreatment(idTratamiento:str, tratamiento:str, costo:str):
    connection()
    try:
        query = ("update tratamientos set Tratamiento=%s, Costo=%s where idTratamiento=%s;")
        val =(tratamiento,costo,idTratamiento)
        cursor.execute(query,val)
        connect.commit()
        return {"Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}

@router.delete("/deleteTreatment")
def deleteTreatment(idTratamiento: str):
    connection()
    try:

        query = "delete from tratamientos where idTratamiento=%s;"
        val = (idTratamiento)
        cursor.execute(query, val)
        connect.commit()
        return {"Eliminado con exito"}
    except Error as e:
        return {"Error: ", e}

