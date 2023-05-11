from config import connect
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor

import plotly.express as px
from enum_translator import translator


def getAllNames():
    db = connect()
    cursor = db.cursor()
    sql = 'SELECT DISTINCT fullname FROM products ORDER BY fullname'
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return [x[0] for x in result]


def getInfo(name):
    db = connect()
    cursor = db.cursor()
    sql = f"SELECT * FROM products WHERE fullname = '{name}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    result.columns = cursor.column_names
    db.close()
    return result


def date_compiler(tble, col):
    ndf = tble.copy().rename(columns={col: 'Date'})
    ndf['day'] = ndf['Date'].dt.day
    ndf['month'] = ndf['Date'].dt.month
    ndf['year'] = ndf['Date'].dt.year
    ndf = ndf.drop(columns='Date')
    return ndf


def usdKztPrdiction():
    f1 = pd.read_csv("USD_KZT Historical Data (4).csv")
    f1['Date'] = pd.to_datetime(f1['Date'], format='%m/%d/%Y')

    regr = GradientBoostingRegressor()
    X = date_compiler(f1[['Date']], 'Date')
    y = f1['Price']
    norm = MinMaxScaler()
    X = norm.fit_transform(X)
    regr.fit(X, y)

    tdf = pd.DataFrame(pd.date_range(start=f1['Date'].min(), end='2023-12-31'))
    y_pred = regr.predict(norm.transform(date_compiler(tdf, 0)))

    toplt1 = f1.copy()
    toplt1['valid'] = 'REAL'
    toplt2 = pd.DataFrame()
    toplt2['Date'] = tdf[0]
    toplt2['Price'] = y_pred
    toplt2['valid'] = 'PREDICTED'
    toplt = pd.concat([toplt1, toplt2]).reset_index().drop(columns='index')

    return toplt


def doPredictionModel(dfs, sdf, st):
    bbs = []
    for x in dfs:
        name = x['fullname'][0]
        if name in translator:
            mode = x['unit'].mode()[0]
            translator[name][mode] = 1
            metrica = st.selectbox(f'Выберите метрику для {name}', translator[name], index=len(translator[name]) - 1)
            for metric in translator[name]:
                x.loc[x['unit'] == metric, 'cost'] = x['cost'] / translator[name][metric]
                x.loc[x['unit'] == metric, 'cost'] = x['cost'] / translator[name][metric]
            x['cost'] = x['cost'] * translator[name][metrica]
            x['unit'] = metrica
        mean = x['cost'].mean()
        x = x[x['cost'] < mean * 2]
        xg = x.groupby('date_contract').mean().reset_index()
        xg['date_contract'] = pd.to_datetime(xg['date_contract'], format='%Y-%m-%d')
        xg['name'] = '(Real)' + name
        bbs.append(xg)
        ss = \
        pd.merge(xg, sdf[sdf['Date'] > xg['date_contract'].min()][~sdf['Date'].duplicated()], left_on='date_contract',
                 right_on='Date', how='right')[['Date', 'cost', 'Price']]
        dates = ss['Date']
        ss = date_compiler(ss, 'Date')
        X = ss.dropna().drop(columns=['cost'])
        y = ss.dropna()['cost']
        norm = MinMaxScaler()
        X = norm.fit_transform(X)
        regr = GradientBoostingRegressor()
        regr.fit(X, y)
        sp = ss.drop(columns=['cost'])
        sp['cost'] = regr.predict(norm.transform(ss.drop(columns=['cost'])))
        sp['date_contract'] = dates
        sp['name'] = '(Predicted)' + name
        bbs.append(sp)
    return px.line(pd.concat(bbs), x="date_contract", y="cost", color='name')


def plotKzt(toplt):
    return px.line(toplt, x="Date", y="Price", color='valid')
