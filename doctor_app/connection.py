import mysql.connector
from mysql.connector import Error


connect = mysql.connector.connect(host="bwqhentfjwvfmwcaipyr-mysql.services.clever-cloud.com", user="uksz5kt6b52dvewr", passwd="IQ2BkXCexmhdQlgHa7yX", db="bwqhentfjwvfmwcaipyr")
cursor = connect.cursor(dictionary=False)


def connection(): #FUNCION PARA HACER CONEXION A BASE DE DATOS
    try:
        if connect.is_connected():
            #db_Info = connection.get_server_info()
            #return {"Connected to MySQL Server version ", db_Info}
            cursor.execute("select database();")
            record = cursor.fetchone()
            return record
    except Error as e:
        return {"Error while connecting to MySQL", e}


def disconnection():
    if connect.is_connected():
        cursor.close()
        connect.close()
        return {"MySQL connection is closed"}


