import pywhatkit
from fastapi import APIRouter


router = APIRouter()
@router.post("/sendMessage")
async def send(phoneN:str, message:str, hour:int, min:int):
    pywhatkit.sendwhatmsg('+52'+phoneN, message, hour,min, 15, True, 15)