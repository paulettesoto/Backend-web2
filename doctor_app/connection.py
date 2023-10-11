import mysql.connector
from mysql.connector import Error


connect = mysql.connector.connect(host="localhost", user="root", passwd="root", db="agendado")
cursor = connect.cursor()


def connection(): #FUNCION PARA HACER CONEXION A BASE DE DATOS
    try:
        if connect.is_connected():
            #db_Info = connection.get_server_info()
            #return {"Connected to MySQL Server version ", db_Info}
            cursor.execute("select database();")
            record = cursor.fetchone()
            return {"You're connected to database: ", record}
    except Error as e:
        return {"Error while connecting to MySQL", e}


def disconnection():
    if connect.is_connected():
        cursor.close()
        connect.close()
        return {"MySQL connection is closed"}

