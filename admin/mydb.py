import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="jadwal_skripsi",
    port="8889"
)

cursor = mydb.cursor()
