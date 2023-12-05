
import pywhatkit
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/sendMessage",
    tags=["Enviar mensaje"],
    responses={404: {"description": "Not found"}})

@router.post("/sendMessage")
async def send(phoneN: str, message: str, hour: int, min: int):
    pywhatkit.sendwhatmsg('+52' + phoneN, message, hour, min, 15, tab_close=True, close_time=1)