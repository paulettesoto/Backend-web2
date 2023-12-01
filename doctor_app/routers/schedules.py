from mysql.connector import Error
from ..connection import connection,disconnection,cursor,connect
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/schedules",
    tags=["Horarios"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.post("/addDates")
def addDates(idDoctor:int, fecha:str, hora:str,status:bool):
    connection()
    try:
        query = ("insert into horarios(idDoctor,fecha,hora,status) values(%s,%s,%s,%s);")
        val =(idDoctor, fecha, hora, status)
        cursor.execute(query,val)
        connect.commit()
        #record = cursor.rowcount()
        #if record is not None:
        return {"Insertado con exito"}
    except Error as e:
        return {"Error: ", e}


@router.get("/availableDates")
def availableDates(idDoctor:str):
    connection()
    try:
        query = ("select * from horarios where idDoctor="+idDoctor+" and status=true and fecha>=curdate() and hora > current_time();")
        #print(query)
        #val = (idDoctor)
        cursor.execute(query)
        record = cursor.fetchall()
        #print(record)
        return record
    except Error as e:
        return {"Error: ", e}


@router.delete("/deleteDates")
def deleteDates(idDoctor:int, fecha:str, hora:str):
    connection()
    try:
        query = ("select idhorarios from horarios where idDoctor=%s  and fecha=%s and hora =%s;")
        val = (idDoctor,fecha,hora)
        cursor.execute(query, val)
        record = cursor.fetchone()
        if record is not None:
            #return {record}
            # disconnection()
            # connection()
            try:
                query = ("delete from horarios where idhorarios=%s;")
                val = (record)
                cursor.execute(query, val)
                connect.commit()
                # record = cursor.rowcount()
                # if record is not None:
                return {"Eliminado con exito"}
            except Error as e:
                disconnection()
                return {"Error: ", e}
    except Error as e:
        disconnection()
        return {"Error: ", e}


