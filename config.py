import psycopg2


def connect():
    return psycopg2.connect(database="nomens",
                            host="dpg-che690t269v75d2ph15g-a",
                            user="nomens_user",
                            password="rx4ra5ixGSZ6uCQyMoMXScaWN36sElkh",
                            port="5432")
    # return mysql.connector.connect(
    #    host="localhost",
    #    user="root",
    #    password="root",
    #    database="nomens",
    #    charset='utf8'
    #)
