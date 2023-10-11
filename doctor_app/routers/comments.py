from mysql.connector import Error
from .connection import connection,disconnection,cursor,connect
from fastapi import APIRouter

router = APIRouter()