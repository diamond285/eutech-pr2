from config import connect
import pandas as pd

def getAllClusters():
    db = connect()
    cursor = db.cursor()
    sql = 'SELECT cluster, count(*) counter FROM clusters GROUP BY cluster ORDER BY counter DESC'
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return [x[0] for x in result]


def getClusterContains(cluster_name):
    db = connect()
    cursor = db.cursor()
    sql = f"SELECT DISTINCT subcluster FROM `clusters` WHERE cluster = '{cluster_name}' ORDER BY subcluster"
    cursor.execute(sql)
    result = [int(x[0]) for x in cursor.fetchall()]
    db.close()
    return min(result), max(result)


def getSubclusterContains(cluster_name, subclust):
    db = connect()
    cursor = db.cursor()
    sql = f"SELECT * FROM `clusters` WHERE cluster = '{cluster_name}' AND subcluster = '{subclust}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    result.columns = cursor.column_names
    db.close()
    return result

