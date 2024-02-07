from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
#from .dependecies import get_token_header
from mysql.connector import Error
from doctor_app.connection import connection, disconnection
from doctor_app.routers import (dates, comments, doctors, clinicalrecords, patientslist, treatments, uploadImages,
                                uploadDocs, sendMessage, pdf, schedules, patientdates, patientcomments, patientdoctors,
                                patient, patientschedule,clinicalrecordsPaciente)
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
app.include_router(patientslist.router)
app.include_router(clinicalrecords.router)
app.include_router(treatments.router)
app.include_router(uploadImages.router)
app.include_router(uploadDocs.router)
app.include_router(sendMessage.router)
app.include_router(pdf.router)
app.include_router(patientdates.router)
app.include_router(patientschedule.router)
app.include_router(patientcomments.router)
app.include_router(patientdoctors.router)
app.include_router(patient.router)
app.include_router(clinicalrecordsPaciente.router)
id = ""
@app.get("/login")
def login(user: str, pswrd: str):
    connect, cursor = connection()
    try:
        cursor.execute("select idDoctor, Nombre, PrimerApe, SegundoApe, Correo from doctor where Celular="+ user + "or Correo="+user+" and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            id_doctor, nombre, primer_ape, segundo_ape, correo = record
            return {
                "id": id_doctor,
                "Nombre": nombre,
                "PrimerApe": primer_ape,
                "SegundoApe": segundo_ape,
                "email": correo
            }
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
        return {"success": "Insertado con éxito"}
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
        return {"success": "Registrado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect,cursor)

@app.get("/login_paciente")
def login(user:str, pswrd:str):
    connect, cursor = connection()
    try:
        cursor.execute("select idPaciente, Nombre, PrimerApe, SegundoApe, FechaNac, Correo from paciente where Celular="+ user + " and Contrasena=" + pswrd + ";")
        record = cursor.fetchone()
        if record is not None:
            id_paciente, nombre, primer_ape, segundo_ape, fecha, correo= record
            return {
                "id": id_paciente,
                "Nombre": nombre,
                "PrimerApe": primer_ape,
                "SegundoApe": segundo_ape,
                "FechaNac": fecha,
                "email": correo
            }
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect,cursor)


if __name__ == "__main__":
    uvicorn.run(app)
