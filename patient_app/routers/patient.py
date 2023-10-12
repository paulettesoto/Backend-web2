from mysql.connector import Error
from ..connection import connection, cursor,connect
from fastapi import APIRouter

router = APIRouter(
    prefix="/patient",
    tags=["Paciente"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)

@router.put("/update_paciente")
def update_paciente(idPaciente:int, Nombre:str, PrimerApe:str, SegundoApe:str, Celular:str,fecha_nac:str, Correo:str):
    connection()
    try:
        query = ("update paciente set Nombre=%s, PrimerApe=%s, SegundoApe=%s, Celular=%s, FechaNac=%s, Correo=%s where idPaciente=%s;")
        val =(Nombre,PrimerApe,SegundoApe,Celular,fecha_nac,Correo,idPaciente)
        cursor.execute(query,val)
        connect.commit()
        return {"Actualizado con exito"}
    except Error as e:
        return {"Error: ", e}

@router.put("/updatePswrd")
def updatePswrd(idPaciente:int, Contrasena_actual:str, ContrasenaNueva:str, verif_contra:str):
    connection()
    try:
        query = ("select * from paciente where idPaciente=%s  and contrasena=%s;")
        val = (idPaciente, Contrasena_actual)
        cursor.execute(query,val)
        record = cursor.fetchone()
        if record is not None:
            try:
                if ContrasenaNueva==verif_contra:
                    query = ("update paciente set Contrasena=%s where idPaciente=%s;")
                    val =(ContrasenaNueva,idPaciente)
                    cursor.execute(query,val)
                    connect.commit()
                    return {"Contraseña actualizada con exito"}
                else:
                    return {"La verificacion de la contraseña no coincide con la contraseña nueva"}
            except Error as e:
                return {"Error: ", e}

    except Error as e:
        return {"Error: ", e}



