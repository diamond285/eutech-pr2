from config import connect
import pandas as pd
import re


def extract_data(data: str):
    s = data.split('\n')
    d = {}
    for x in s:
        if ':' in x:
            atr, val = (x.replace(';', '').strip() for x in x.split(':', 1))
            if re.match('^\d+\.', atr):
                atr = atr.split('.', 1)[1]
            if re.match('^\d+\)', atr):
                atr = atr.split(')', 1)[1]
            if re.match('\-\ ', atr):
                atr = atr.split('-', 1)[1]
            if val == '':
                continue
            d[atr.strip()] = val.strip()
    return d


def getParams(name):
    db = connect()
    cursor = db.cursor()
    sql = f"SELECT * FROM `parameters` WHERE fullname = '{name}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    result.columns = cursor.column_names
    db.close()
    return extract_data(result['gpt'][0].decode("utf-8"))
