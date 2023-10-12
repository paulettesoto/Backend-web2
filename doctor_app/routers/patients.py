from mysql.connector import Error
from  ..connection import (connection, cursor,connect)
from fastapi import APIRouter

#from ..dependecies import get_token_header
#from..main import idDoctor

router = APIRouter(
    prefix="/patients",
    tags=["Pacientes"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)