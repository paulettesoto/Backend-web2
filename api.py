from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
app = FastAPI()


connect = mysql.connector.connect(host="localhost", user="root", passwd="root", db="agendado")
cursor = connect.cursor()


@app.get("/connection")
def connection(): #FUNCION PARA HACER CONEXION A BASE DE DATOS
    try:
        if connect.is_connected():
            #db_Info = connection.get_server_info()
            #return {"Connected to MySQL Server version ", db_Info}
            cursor.execute("select database();")
            record = cursor.fetchone()
            return {"You're connected to database: ", record}
    except Error as e:
        return {"Error while connecting to MySQL", e}


@app.get("/disconnection")
def disconnection():
    if connect.is_connected():
        cursor.close()
        connect.close()
        return {"MySQL connection is closed"}


@app.get("/login")
def login(user:str, pswrd:str):
    connection()
    try:
        cursor.execute("select * from doctor where Celular="+ user + " and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            return {record}
    except Error as e:
        return {"Error: ", e}
    disconnection()


@app.get("/signIn")
def signIn(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, Especialidad:str, Correo:str, Cedula:str, HojaDoctor:str, Contrasena:str, Foto:str):
    connection()
    try:
        query = ("insert into doctor(Nombre,PrimerApe,SegundoApe,Celular,Especialidad,Correo,Cedula,"
                 "HojaDoctor,Contrasena,Foto) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);")
        val =(Nombre,PrimerApe,SegundoApe,Celular,Especialidad,Correo,Cedula,HojaDoctor,Contrasena,Foto)
        cursor.execute(query,val)
        connect.commit()
        #record = cursor.rowcount()
        #if record is not None:
        return {"Insertado con exito"}
    except Error as e:
        return {"Error: ", e}
    disconnection()


@app.get("/update")
def update(idDoctor:int, Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, Especialidad:str, Correo:str, Cedula:str, HojaDoctor:str, Foto:str):
    connection()
    try:
        query = ("update doctor set Nombre=%s, PrimerApe=%s, SegundoApe=%s, Celular=%s, Especialidad=%s, Correo=%s, Cedula=%s,"
                 "HojaDoctor=%s, Foto=%s where idDoctor=%s;")
        val =(Nombre,PrimerApe,SegundoApe,Celular,Especialidad,Correo,Cedula,HojaDoctor,Foto,idDoctor)
        cursor.execute(query,val)
        connect.commit()
        #record = cursor.rowcount()
        #if record is not None:
        return {"Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}
    disconnection()


@app.get("/updatePswrd")
def updatePswrd(idDoctor:int, Contrasena:str, ContrasenaNueva:str):
    connection()
    try:
        query = ("select * from doctor where idDoctor=%s  and Contrasena=%s;")
        val = (idDoctor, Contrasena)
        cursor.execute(query,val)
        record = cursor.fetchone()
        if record is not None:
            #return {record}
            #disconnection()
            #connection()
            try:
                query = ("update doctor set Contrasena=%s where idDoctor=%s;")
                val =(ContrasenaNueva,idDoctor)
                cursor.execute(query,val)
                connect.commit()
                #record = cursor.rowcount()
                #if record is not None:
                return {"Contraseña actualizada con exito"}
            except Error as e:
                return {"Error: ", e}
        disconnection()
    except Error as e:
        return {"Error: ", e}
    disconnection()


@app.get("/addDates")
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


@app.get("/availableDates")
def availableDates(idDoctor:str):
    connection()
    try:
        query = ("select * from horarios where idDoctor="+idDoctor+" and status=true;")
        #print(query)
        #val = (idDoctor)
        cursor.execute(query)
        record = cursor.fetchall()
        #print(record)
        return record
    except Error as e:
        return {"Error: ", e}


@app.get("/deleteDates")
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

