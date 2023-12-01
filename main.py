from fastapi import FastAPI
import uvicorn
#from .dependecies import get_token_header
from mysql.connector import Error
from doctor_app.connection import connection,cursor,connect
from doctor_app.routers import (dates, comments, doctors, clinicalrecords, patients, treatments, uploadImages,
                                uploadDocs, sendMessage, pdf, schedules, patientdates, patientcomments, patientdoctors, patient,schedule)
#from localStoragePy import localStoragePy

#localStorage = localStoragePy('agendado', 'text')
app = FastAPI()
app.include_router(dates.router)
app.include_router(schedules.router)
app.include_router(comments.router)
app.include_router(doctors.router)
app.include_router(clinicalrecords.router)
app.include_router(patients.router)
app.include_router(treatments.router)
app.include_router(uploadImages.router)
app.include_router(uploadDocs.router)
app.include_router(sendMessage.router)
app.include_router(pdf.router)
app.include_router(patientdates.router)
app.include_router(schedule.router)
app.include_router(patientcomments.router)
app.include_router(patientdoctors.router)
app.include_router(patient.router)
idDoctor = ""
@app.get("/login")
def login(user:str, pswrd:str):
    connection()
    try:
        cursor.execute("select idDoctor from doctor where Celular="+ user + " and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            idDoctor = record
            return record
    except Error as e:
        return {"Error: ", e}


@app.post("/signUp")
def signUp(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, Especialidad:str, Correo:str,
           Cedula:str, HojaDoctor:str, Contrasena:str, Foto:str):
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


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
