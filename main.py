import pandas as pd
import streamlit as st
import cluster
from clusts import clusts
import parameters
import regression
from imaginator import get_google_img

def __main__():
    tab1, tab2, tab3 = st.tabs(["Кластеры", "Прогноз цены", "Owl"])

    with tab1:
        st.header("Итоги кластерзации")
        values = clusts
        option = st.selectbox(
            'Выберите категорию',
            values
        )
        mini, maxi = cluster.getClusterContains(option)
        tab1_1, tab1_2 = st.tabs(["Все", "Эталонные значения"])
        with tab1_1:
            if mini == maxi:
                for x in cluster.getSubclusterContains(option, -1).iloc:
                    st.write(x['fullname'])
                    l = dict(x)
                    d = parameters.getParams(x['fullname'])
                    for i in d:
                        l[i] = d[i]
                    st.write(l)
            else:
                cluster_num = st.slider(
                    'Выберите кластер', mini, maxi
                )
                for x in cluster.getSubclusterContains(option, cluster_num).iloc:
                    st.write(x['fullname'])
                    l = dict(x)
                    d = parameters.getParams(x['fullname'])
                    for i in d:
                        l[i] = d[i]
                    st.write(l)
        with tab1_2:
            max_val = []
            max_len = 0
            for cluster_i in cluster.getClusterContains(option):
                for x in cluster.getSubclusterContains(option, cluster_i).iloc:
                    l = dict(x)
                    d = parameters.getParams(x['fullname'])
                    for i in d:
                        l[i] = d[i]
                    if len(l) > max_len:
                        max_val = l
                        max_len = len(l)
            st.write(max_val['fullname'])
            st.write(max_val)

    with tab2:
        values = regression.getAllNames()
        selected = st.multiselect(
            'Введите наименование',
            values
        )
        df = []
        for x in selected:
            tmp = regression.getInfo(x)
            if len(tmp) < 10:
                st.write(x + ":  \nПрогноз невозможен, слишком мало данных по выбранному номенклатуре, Прогноз по остальным номенклатурам ниже")
                st.write(tmp)
            else:
                df.append(tmp)
        tdf = regression.usdKztPrdiction()
        if df:
            st.plotly_chart(regression.doPredictionModel(df, tdf, st))
        st.subheader("USD/KZT prediction")
        st.plotly_chart(regression.plotKzt(tdf))

    with tab3:
        st.header(option)
        if option == 'труба':
            st.image(get_google_img("дудец", st), width=200)
        else:
            st.subheader(x['fullname'])
            st.image(get_google_img(x['fullname'], st), width=200)


__main__()
