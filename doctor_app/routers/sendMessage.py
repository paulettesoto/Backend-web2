#import pywhatkit
from fastapi import APIRouter, Depends, HTTPException
#from twilio.rest import Client
import webbrowser
router = APIRouter(
    prefix="/sendMessage",
    tags=["Enviar mensaje"],
    responses={404: {"description": "Not found"}})

# Configuración de Twilio
#account_sid = "ACef3aa565fe7150e6f252bd6ce108646f"
#auth_token = "ba620d466f1a3b1377b328803ba3b490"
#client = Client(account_sid, auth_token)

@router.post("/sendMessage")
async def send(phoneN: str, text: str):
    whatsapp_phone_number = "52" + phoneN
    try:
        # Enlace de WhatsApp
        whatsapp_link = 'https://api.whatsapp.com/send/?phone=' +whatsapp_phone_number+ '&text=' +text+ '&type=phone_number&app_absent=0'

        # Abrir el enlace en el navegador predeterminado
        webbrowser.open(whatsapp_link)
        return {"success": "Mensaje enviado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        #pywhatkit.sendwhatmsg('+52' + phoneN, message, hour, min, 15, tab_close=False)




