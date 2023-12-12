import mysql.connector
from mysql.connector import Error





def connection(): #FUNCION PARA HACER CONEXION A BASE DE DATOS
    connect = mysql.connector.connect(host="bwqhentfjwvfmwcaipyr-mysql.services.clever-cloud.com", port="3306",
                                      user="uksz5kt6b52dvewr", passwd="IQ2BkXCexmhdQlgHa7yX", db="bwqhentfjwvfmwcaipyr")
    #connect = mysql.connector.connect(host="bwqhentfjwvfmwcaipyr-mysql.services.clever-cloud.com", port="3306",
     #                               user = "uksz5kt6b52dvewr", passwd = "IQ2BkXCexmhdQlgHa7yX", db = "bwqhentfjwvfmwcaipyr")
    cursor = connect.cursor(dictionary=False)
    try:
        if connect.is_connected():
            #db_Info = connection.get_server_info()
            #return {"Connected to MySQL Server version ", db_Info}
            cursor.execute("select database();")
            record = cursor.fetchone()
            return connect, cursor
    except Error as e:
        return {"Error: ", e}


#def disconnection(connect, cursor):
#    if connect.is_connected():
#        cursor.close()
#        connect.close()
#        return {"MySQL connection is closed"}


def disconnection(connect, cursor):
    try:
        if connect.is_connected():
            if cursor.with_rows:
                cursor.fetchall()

            cursor.close()

            connect.commit()

            connect.close()

            return {"success": "MySQL connection is closed"}

    except mysql.connector.Error as e:
        return {"Error: ", e}

