from mysql.connector import Error
from .connection import connection,disconnection,cursor,connect
from fastapi import APIRouter, Depends
from ..dependecies import get_token_header

router = APIRouter(
    prefix="/patients",
    tags=["Pacientes"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)