from mysql.connector import Error
from ..connection import connection, disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/clinicalRecords-answers",
    tags=["Historia Clinica Respuestas"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("/clinicalRecords-answers")
def getAnswers(idDoctor:str, idPaciente:str, cuenta:int):
    connect, cursor = connection()
    try:
        query = ("select r.idrespuesta, c.Pregunta, r.doctor_idDoctor, r.paciente_idPaciente, r.respuesta "
                 "from respuestas as r inner join historiaclinica as c on c.idhistoriaClinica = r.historiaclinica_idhistoriaClinica"
                 " where doctor_idDoctor=" + idDoctor + " and paciente_idPaciente=" + idPaciente +" and cuenta=%s;")
        val=(cuenta,)
        cursor.execute(query, val)
        records = cursor.fetchall()

        if records:
            clinical_records_Answer_list = []
            for record in records:
                id, pregunta, iddoctor, idPaciente, respuesta= record
                clinical_records_Answer_dict = {
                    "id": id,
                    "pregunta": pregunta,
                    "doctor": iddoctor,
                    "paciente": idPaciente,
                    "respuesta": respuesta
                }
                clinical_records_Answer_list.append(clinical_records_Answer_dict)

            return {"clinicalRecordsAnswers": clinical_records_Answer_list}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)


@router.post("/addAnswer")
def addAnswer(idQ:str,idDoctor:str,Ans:str,idPaciente:str, cuenta:int):
    connect, cursor = connection()
    try:
        query = ("insert into respuestas(historiaclinica_idhistoriaClinica,doctor_idDoctor,paciente_idPaciente,respuesta, cuenta) values(%s,%s,%s,%s, %s);")
        val =(idQ,idDoctor,idPaciente,Ans, cuenta)
        cursor.execute(query,val)
        connect.commit()
        return {"success": "Registrado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.put("/updateAns")
def updateAns(idAns:str, ans:str):
    connect, cursor = connection()
    try:
        query = ("update respuestas set respuesta=%s where idrespuesta=%s;")
        val =(ans,idAns)
        cursor.execute(query,val)
        connect.commit()
        return {"success": "Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)

@router.delete("/deleteAns")
def deleteAns(idAns: str):
    connect, cursor = connection()
    try:

        query = "delete from respuestas where idrespuesta="+idAns+";"
        cursor.execute(query)
        connect.commit()
        return {"success": "Eliminado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)



