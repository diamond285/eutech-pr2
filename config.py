import mysql


def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="nomens",
        charset='utf8'
    )
