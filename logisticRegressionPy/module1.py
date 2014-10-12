import mysql.connector
from mysql.connector import errorcode

user = 'test_user'
password = 'test01'
host = '127.0.0.1'
database = 'tws_server'
port = 3308

try:
    cnx = mysql.connector.connect(host, user, password, database, port)

    cursor = cnx.cursor()

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)

#cursor.execute(query)

#for contract_symbol in cursor:
#  print(contract_symbol)

#cursor.close()

#cnx.close()