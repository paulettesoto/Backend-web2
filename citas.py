from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
from main import connection, disconnection
app = FastAPI()


connect = mysql.connector.connect(host="localhost", user="root", passwd="root", db="agendado")
cursor = connect.cursor()


@app.get("/setDate")
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
                query = ("insert into cita(Paciente_idPaciente,Doctor_idDoctor,idTratamiento,idHorario) values("+ idPaciente +","+ idDoctor +","+ idTratamiento +",%s);")
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


#@app.get("/cancelDate")