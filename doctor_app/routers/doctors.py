from mysql.connector import Error
from ..connection import connection,disconnection
from fastapi import APIRouter

#from ..dependecies import get_token_header

router = APIRouter(
    prefix="/doctors",
    tags=["Doctores"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

@router.put("/update")
def update(idDoctor:int, Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str, Especialidad:str, Correo:str,
           Cedula:str, HojaDoctor:str, Foto:str):
    connect, cursor = connection()
    try:
        query = ("update doctor set Nombre=%s, PrimerApe=%s, SegundoApe=%s, Celular=%s, Especialidad=%s, "
                 "Correo=%s, Cedula=%s,HojaDoctor=%s, Foto=%s where idDoctor=%s;")
        val =(Nombre,PrimerApe,SegundoApe,Celular,Especialidad,Correo,Cedula,HojaDoctor,Foto,idDoctor)
        cursor.execute(query,val)
        connect.commit()
        #record = cursor.rowcount()
        #if record is not None:
        return {"success": "Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)



@router.put("/updatePswrd")
def updatePswrd(idDoctor:int, Contrasena:str, ContrasenaNueva:str,verif_contra:str):
    connect, cursor = connection()
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
                if ContrasenaNueva == verif_contra:
                    query = ("update doctor set Contrasena=%s where idDoctor=%s;")
                    val =(ContrasenaNueva,idDoctor)
                    cursor.execute(query,val)
                    connect.commit()
                #record = cursor.rowcount()
                #if record is not None:
                    return {"success": "Contraseña actualizada con exito"}
                else:
                    return {"Error": "La verificacion de la contraseña no coincide con la contraseña nueva"}
            except Error as e:
                return {"Error: ", e}
            finally:
                disconnection(connect, cursor)
    except Error as e:
        return {"Error: ", e}
    finally:
        disconnection(connect, cursor)
