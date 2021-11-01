import pandas as pd
import streamlit as st
from pandas.core.frame import DataFrame
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

csv = 'COP_USD.csv'
df = 0

def punto1():
    global df, csv
    df = pd.read_csv(csv, sep=';', thousands=',')
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Diferencia'] = df['Diferencia'].str.rstrip('%').astype('float') / 100.0
    st.header("Punto 1:")
    st.subheader("DataFrame->COP_USD.")
    st.dataframe(df.set_index('Fecha'))

def punto2():
    global df
    st.header("Punto 2:")
    st.subheader("Grafica Precio.")
    st.line_chart(df.set_index('Fecha')['Precio'])

def punto3():
    global df
    st.header("Punto 3:")
    st.subheader("DataFrame con corrección de datos faltantes.")
    df = df.interpolate(method='ffill', limit_direction='forward')
    df = df.fillna(method='bfill')
    df = df.fillna(method='pad')
    st.dataframe(df.set_index('Fecha'))

def punto4():
    global df
    st.header("Punto 4:")
    st.subheader("Verificacion de datos.")
    st.dataframe((df.set_index('Fecha')).isnull())


def punto5():
    st.header("Punto 5:")
    st.subheader("Seleccion de rango de tiempo para visualizacion.")
    inicial, final = st.columns(2)
    with inicial:
        dato_inicial = st.date_input("Fecha initial: ", min_value=datetime.date(1990, 1, 2))
        dato_inicial = str(dato_inicial)

    with final:
        dato_final = st.date_input("Fecha final: ")
        dato_final = str(dato_final)
    global df_temporal
    df_temporal = df.set_index('Fecha').loc[dato_inicial:dato_final, 'Precio':'Diferencia']
    st.write(df_temporal)

def punto6():
    st.header("Punto 6:")
    st.subheader("Promedios, Maximos y Mínimos para cada ventana temporal.")
    global df_temporal, df_resumen
    df_max = df_temporal.max()
    df_min = df_temporal.min()
    df_prom = df_temporal.mean()
    df_resumen = DataFrame([df_min, df_max, df_prom], index=['Minimos', 'Maximos', 'Promedios'])
    st.dataframe(df_resumen)

def punto7():
    st.header("Punto 7:")
    st.subheader("Calculo de Mediana para ventana temporal por mes.")
    global df
    df_mes_mediana = df.set_index('Fecha').resample('M').median()
    st.dataframe(df_mes_mediana)
    st.line_chart(df_mes_mediana['Precio'])

def punto8():
    global df_resumen
    st.header("Punto 8:")
    st.subheader("Calculo de Desviacion Estandar para ventana temporal.")
    df_temporal1 = DataFrame(df_resumen.std())
    st.dataframe(df_temporal1.transpose())

def punto9():
    st.header("Punto 9:")
    st.subheader("Calculo de las desviaciones estándar para cada mes y año.")
    st.subheader("Desviacion estándar para cada mes")
    st.text("Meses con mayores desviacion")
    df_mes_std = df.set_index('Fecha').resample('M').std()
    st.dataframe(df_mes_std.sort_values(by=['Precio', 'Apertura', 'Maximo', 'Minimo', 'Diferencia'], ascending=False).head())
    st.text("Meses con menores desviacion")
    st.dataframe(df_mes_std.sort_values(by=['Precio', 'Apertura', 'Maximo', 'Minimo', 'Diferencia'], ascending=False).tail())
    st.subheader("Desviacion estándar para cada año")
    st.text("Años con mayores desviacion")
    df_año_std = df.set_index('Fecha').resample('Y').std()
    st.dataframe(df_año_std.sort_values(by=['Precio', 'Apertura', 'Maximo', 'Minimo', 'Diferencia'], ascending=False).head())
    st.text("Años con menores desviacion")
    st.dataframe(df_año_std.sort_values(by=['Precio', 'Apertura', 'Maximo', 'Minimo', 'Diferencia'], ascending=False).tail())

def punto10():
    st.header("Punto 10:")
    st.subheader("Suma de las diferencias por año.")
    global df
    columna3, columna4 = st.columns(2)
    with columna3:
        df_diferencia_año = df.set_index('Fecha')['Diferencia'].resample('Y').sum()
        st.dataframe(df_diferencia_año.sort_values(ascending=False))
    with columna4:
        st.text("Años con menor devaluacion: ")
        st.write(df_diferencia_año.min())
        st.text("Años con mayor devaluacion: ")
        st.write(df_diferencia_año.max())

def main():
    st.title("Taller 1 Analitica Descriptiva.")
    punto1()
    punto2()
    punto3()
    punto4()
    punto5()
    punto6()
    punto7()
    punto8()
    punto9()
    punto10()

if __name__ == '__main__':
    main()