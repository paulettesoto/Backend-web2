from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
from main import connection, disconnection

app = FastAPI()


connect = mysql.connector.connect(host="localhost", user="root", passwd="root", db="agendado")
cursor = connect.cursor()