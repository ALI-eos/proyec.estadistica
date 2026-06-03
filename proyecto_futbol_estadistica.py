
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

ARCHIVO_CSV = "datos_futbol.csv"

def tabla_frecuencia(serie):
    freq = serie.value_counts().sort_index()
    tabla = pd.DataFrame({
        "fi": freq,
        "Fi": freq.cumsum()
    })
    tabla["hi"] = tabla["fi"] / tabla["fi"].sum()
    tabla["%"] = tabla["hi"] * 100
    tabla["Hi"] = tabla["hi"].cumsum()
    return tabla

def tabla_agrupada(serie):
    n = len(serie)
    k = max(4, int(round(1 + 3.322 * np.log10(n))))
    intervalos = pd.cut(serie, bins=k)
    freq = intervalos.value_counts().sort_index()

    tabla = pd.DataFrame({
        "fi": freq,
        "Fi": freq.cumsum()
    })
    tabla["hi"] = tabla["fi"] / tabla["fi"].sum()
    tabla["%"] = tabla["hi"] * 100
    tabla["Marca"] = [
        round((x.left + x.right)/2, 2)
        for x in intervalos.cat.categories
    ]

    tabla.index = [
        f"{x.left:.0f}-{x.right:.0f}"
        for x in intervalos.cat.categories
    ]

    info = {
        "n": n,
        "minimo": serie.min(),
        "maximo": serie.max(),
        "rango": serie.max() - serie.min(),
        "k": k
    }
    return tabla, info

def medidas(serie):
    return pd.DataFrame({
        "Medida": [
            "Media","Mediana","Moda",
            "Varianza","Desv. estándar",
            "Máximo","Mínimo","Rango"
        ],
        "Valor": [
            serie.mean(),
            serie.median(),
            serie.mode().iloc[0],
            serie.var(),
            serie.std(),
            serie.max(),
            serie.min(),
            serie.max()-serie.min()
        ]
    })

def cargar_datos():
    return pd.read_csv(ARCHIVO_CSV)

def ejecutar_terminal():
    df = cargar_datos()

    print("="*60)
    print("ESTADÍSTICA DESCRIPTIVA - FÚTBOL")
    print("="*60)

    print("\nBASE DE DATOS")
    print(df.head(15))
    print("\nTotal registros:", len(df))

    print("\nVARIABLE CUALITATIVA: POSICIÓN")
    tabla_pos = tabla_frecuencia(df["Posicion"])
    print(tabla_pos)

    plt.figure(figsize=(7,4))
    plt.bar(tabla_pos.index.astype(str), tabla_pos["fi"])
    plt.title("Frecuencia de posiciones")
    plt.grid(True)
    plt.show(block=True)

    plt.figure(figsize=(6,6))
    plt.pie(tabla_pos["fi"], labels=tabla_pos.index, autopct="%1.1f%%")
    plt.title("Distribución de posiciones")
    plt.show(block=True)

    print("\nVARIABLE DISCRETA: GOLES")
    tabla_goles = tabla_frecuencia(df["Goles"])
    print(tabla_goles)
    print(medidas(df["Goles"]))

    plt.figure(figsize=(7,4))
    plt.stem(tabla_goles.index, tabla_goles["fi"])
    plt.title("Goles anotados")
    plt.grid(True)
    plt.show(block=True)

    print("\nVARIABLE CONTINUA: EDAD")
    tabla_edad, info = tabla_agrupada(df["Edad"])
    print(info)
    print(tabla_edad)

    plt.figure(figsize=(7,4))
    plt.hist(df["Edad"], bins=info["k"])
    plt.title("Histograma edades")
    plt.grid(True)
    plt.show(block=True)

    plt.figure(figsize=(7,4))
    plt.plot(tabla_edad["Marca"], tabla_edad["fi"], marker="o")
    plt.title("Polígono de frecuencia")
    plt.grid(True)
    plt.show(block=True)

    plt.figure(figsize=(7,4))
    plt.plot(tabla_edad["Marca"], tabla_edad["Fi"], marker="o")
    plt.title("Ojiva")
    plt.grid(True)
    plt.show(block=True)

def ejecutar_streamlit():
    st.set_page_config(page_title="Fútbol Estadística", layout="wide")
    st.title("⚽ Estadística descriptiva del fútbol")

    df = cargar_datos()
    st.subheader("Base de datos")
    st.dataframe(df)
    st.write("Registros:", len(df))

    st.header("Variable cualitativa: Posición")
    tabla_pos = tabla_frecuencia(df["Posicion"])
    st.dataframe(tabla_pos)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.bar(tabla_pos.index.astype(str), tabla_pos["fi"])
    ax.set_title("Frecuencia de posiciones")
    ax.grid(True)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(tabla_pos["fi"], labels=tabla_pos.index, autopct="%1.1f%%")
    ax.set_title("Distribución de posiciones")
    st.pyplot(fig)

    st.header("Variable discreta: Goles")
    tabla_goles = tabla_frecuencia(df["Goles"])
    st.dataframe(tabla_goles)
    st.dataframe(medidas(df["Goles"]))

    fig, ax = plt.subplots(figsize=(7,4))
    ax.stem(tabla_goles.index, tabla_goles["fi"])
    ax.set_title("Goles anotados")
    ax.grid(True)
    st.pyplot(fig)

    st.header("Variable continua: Edad")
    tabla_edad, info = tabla_agrupada(df["Edad"])
    st.write(info)
    st.dataframe(tabla_edad)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.hist(df["Edad"], bins=info["k"])
    ax.set_title("Histograma edades")
    ax.grid(True)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(tabla_edad["Marca"], tabla_edad["fi"], marker="o")
    ax.set_title("Polígono de frecuencia")
    ax.grid(True)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(tabla_edad["Marca"], tabla_edad["Fi"], marker="o")
    ax.set_title("Ojiva")
    ax.grid(True)
    st.pyplot(fig)

if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx():
            ejecutar_streamlit()
        else:
            ejecutar_terminal()
    except Exception:
        ejecutar_terminal()
