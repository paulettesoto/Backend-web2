import pywhatkit
import os
from fastapi import APIRouter, Depends
#from ..dependecies import get_token_header


router = APIRouter(
    prefix="/sendMessage",
    tags=["Enviar mensaje"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


@router.post("/sendMessage")
async def send(phoneN:str, message:str, hour:int, min:int):
    try:
        display_var = os.environ['DISPLAY']
        pywhatkit.sendwhatmsg('+52' + phoneN, message, hour, min, 15, tab_close=True, close_time=1)
    # Código que utiliza pywhatkit
    except KeyError:
        # Manejar la excepción, por ejemplo, imprimir un mensaje o tomar una acción alternativa
        print("No se encontró la variable de entorno 'DISPLAY'. Verifica si estás en un entorno gráfico.")


