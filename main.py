from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
#from .dependecies import get_token_header
from mysql.connector import Error
from doctor_app.connection import connection, disconnection
from doctor_app.routers import (dates, comments, doctors, clinicalrecords, patients, treatments, uploadImages,
                                uploadDocs, sendMessage, pdf, schedules, patientdates, patientcomments, patientdoctors, patient,schedule)
#from localStoragePy import localStoragePy

#localStorage = localStoragePy('agendado', 'text')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def login(user: str, pswrd: str):
    connect, cursor = connection()
    try:
        cursor.execute("select idDoctor from doctor where Celular="+ user + " and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            idDoctor = record
            return idDoctor
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect,cursor)



@app.post("/signUp")
def signUp(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, Especialidad:str, Correo:str,
           Cedula:str, HojaDoctor:str, Contrasena:str, Foto:str):
    connect, cursor = connection()
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
    finally:
        disconnection(connect,cursor)


@app.post("/signUp_paciente")
def signIn_paciente(Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, fecha_nac:str, Correo:str, Contrasena:str, confirmar_contra:str):
    connect, cursor = connection()
    try:
        if(Contrasena==confirmar_contra):
            query = ("insert into paciente(Nombre,PrimerApe,SegundoApe,Celular,FechaNac,Correo,Contrasena) values(%s,%s,%s,%s,%s,%s,%s);")
            val =(Nombre,PrimerApe,SegundoApe,Celular,fecha_nac,Correo,Contrasena)
            cursor.execute(query,val)
            connect.commit()
        return {"Registrado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect,cursor)

@app.get("/login_paciente")
def login(user:str, pswrd:str):
    connect, cursor = connection()
    try:
        cursor.execute("select * from paciente where Celular="+ user + " and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            return {record}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect,cursor)


if __name__ == "__main__":
    uvicorn.run(app)
