from config import connect
import pandas as pd


def getAllClusters():
    db = connect()
    cursor = db.cursor()
    sql = 'SELECT cluster, count(*) counter FROM clusters GROUP BY cluster ORDER BY counter DESC'
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return result


def getClusterContains(cluster_name):
    db = connect()
    cursor = db.cursor()
    sql = f"SELECT DISTINCT subcluster FROM clusters WHERE cluster = '{cluster_name}' ORDER BY subcluster"
    cursor.execute(sql)
    result = [int(x[0]) for x in cursor.fetchall()]
    db.close()
    return min(result), max(result)


def getSubclusterContains(cluster_name, subclust):
    db = connect()
    cursor = db.cursor()
    sql = f"SELECT * FROM clusters c join parameters p on c.fullname = p.fullname WHERE cluster = '{cluster_name}' AND subcluster = '{subclust}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    result.columns = [desc[0] for desc in cursor.description]
    db.close()
    return result


def getMaxClusterContains(cluster_name):
    db = connect()
    cursor = db.cursor()
    sql = f"select * from clusters c join parameters p on c.fullname = p.fullname where cluster = '{cluster_name}' and p.paramcount = (select max(paramcount) from clusters c join parameters p on c.fullname = p.fullname where cluster = '{cluster_name}');"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    result.columns = [desc[0] for desc in cursor.description]
    db.close()
    return result
