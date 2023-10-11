from fastapi import FastAPI, Depends
from .dependecies import get_token_header
from mysql.connector import Error
from .connection import connection, cursor,connect
from .routers import dates, comments, doctors, clinicalrecords, patients, treatments,uploadImages,uploadDocs,sendMessage


app = FastAPI()
app.include_router(dates.router)
app.include_router(comments.router)
app.include_router(doctors.router)
app.include_router(clinicalrecords.router)
app.include_router(patients.router)
app.include_router(treatments.router)
app.include_router(uploadImages.router)
app.include_router(uploadDocs.router)
app.include_router(sendMessage.router)


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


@app.post("/signUp")
def signUp(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, Especialidad:str, Correo:str, Cedula:str, HojaDoctor:str, Contrasena:str, Foto:str):
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


