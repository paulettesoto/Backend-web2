from fastapi import FastAPI
#from .dependecies import get_token_header
from mysql.connector import Error
from .connection import connection,cursor,connect
from .routers import (dates, comments, doctors, patient,schedule)
#from localStoragePy import localStoragePy

#localStorage = localStoragePy('agendado', 'text')
app = FastAPI()
app.include_router(dates.router)
app.include_router(schedule.router)
app.include_router(comments.router)
app.include_router(doctors.router)
app.include_router(patient.router)

@app.post("/signUp_paciente")
def signIn_paciente(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, fecha_nac:str, Correo:str, Contrasena:str, confirmar_contra:str):
    connection()
    try:
        if(Contrasena==confirmar_contra):
            query = ("insert into paciente(Nombre,PrimerApe,SegundoApe,Celular,FechaNac,Correo,Contrasena) values(%s,%s,%s,%s,%s,%s,%s);")
            val =(Nombre,PrimerApe,SegundoApe,Celular,fecha_nac,Correo,Contrasena)
            cursor.execute(query,val)
            connect.commit()
        return {"Registrado con exito"}
    except Error as e:
        return {"Error: ", e}

@app.get("/login_paciente")
def login(user:str, pswrd:str):
    connection()
    try:
        cursor.execute("select * from paciente where Celular="+ user + " and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            return {record}
    except Error as e:
        return {"Error: ", e}


