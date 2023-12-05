#import pywhatkit
from fastapi import APIRouter, Depends, HTTPException
from twilio.rest import Client
router = APIRouter(
    prefix="/sendMessage",
    tags=["Enviar mensaje"],
    responses={404: {"description": "Not found"}})

# Configuración de Twilio
account_sid = "ACef3aa565fe7150e6f252bd6ce108646f"
auth_token = "8befb773fd514ccb8b7743476f167893"
client = Client(account_sid, auth_token)

@router.post("/sendMessage")
async def send(phoneN: str, text: str):
    whatsapp_phone_number = "whatsapp:+52" + phoneN  # E.g., "whatsapp:+123456789"
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=text,
            to='whatsapp:+521'+phoneN
        )
        return {"status": "Mensaje enviado", "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        #pywhatkit.sendwhatmsg('+52' + phoneN, message, hour, min, 15, tab_close=False)

