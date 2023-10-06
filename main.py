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