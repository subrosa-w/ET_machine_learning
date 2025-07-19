from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import Response
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
import csv

app = FastAPI()

# Habilitar CORS para el frontend en localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta al archivo CSV
CSV_PATH = os.path.join("public", "CSV", "csgo.csv")  # Cambia a 'data.csv' si lo renombras

def get_df():
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        sample = f.read(2048)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
            delimiter = dialect.delimiter
        except Exception:
            delimiter = ','  # Por defecto, coma
        df = pd.read_csv(f, delimiter=delimiter)
        return df.head(2000)  # Limitar a las primeras 2000 filas

@app.get("/api/summary")
def summary():
    df = get_df()
    return df.head().to_dict(orient="records")

@app.get("/api/columns")
def columns():
    df = get_df()
    return list(df.select_dtypes(include='number').columns)

@app.get("/api/histogram")
def histogram(column: str = Query(...)):
    print(f"Entrando a histogram para columna: {column}")
    df = get_df()
    print("CSV cargado (histogram)")
    if column not in df.columns:
        return JSONResponse({"error": "Columna no encontrada"}, status_code=400)
    plt.figure()
    df[column].dropna().hist(bins=10)  # Menos bins
    plt.title(f"Histograma de {column}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (histogram)")
    return {"img": img_base64}

@app.get("/api/describe")
def describe():
    df = get_df()
    desc = df.describe(include='all').fillna("").to_dict()
    return desc

@app.get("/api/corr")
def corr():
    print("Entrando a corr")
    df = get_df()
    print("CSV cargado (corr)")
    num_df = df.select_dtypes(include='number')
    plt.figure(figsize=(6,4))
    ax = sns.heatmap(num_df.corr(), annot=False, cmap='coolwarm')  # Sin annot
    plt.title("Heatmap de correlación", fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (corr)")
    return {"img": img_base64}

@app.get("/api/corr_inicial")
def corr_inicial():
    print("Entrando a corr_inicial")
    df = get_df()
    print("CSV cargado (corr_inicial)")
    cols = [
        'MatchAssists', 'MatchKills','RoundHeadshots', 'RoundKills',
        'RNonLethalGrenadesThrown','RLethalGrenadesThrown',
        'PrimaryAssaultRifle', 'PrimarySniperRifle','PrimaryHeavy', 'PrimarySMG', 'PrimaryPistol',
    ]
    correlacion_inicial = df[cols].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlacion_inicial, annot=False, cmap='coolwarm', fmt=".2f")  # Sin annot
    plt.title('Correlación entre Variables Inicial')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (corr_inicial)")
    return {"img": img_base64}

@app.get("/api/barplot")
def barplot(column: str = Query(...)):
    print(f"Entrando a barplot para columna: {column}")
    df = get_df()
    print("CSV cargado (barplot)")
    if column not in df.columns:
        return JSONResponse({"error": "Columna no encontrada"}, status_code=400)
    plt.figure()
    df[column].value_counts().plot(kind='bar')
    plt.title(f"Barplot de {column}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (barplot)")
    return {"img": img_base64}

@app.get("/api/boxplot")
def boxplot(column: str = Query(...)):
    print(f"Entrando a boxplot para columna: {column}")
    df = get_df()
    print("CSV cargado (boxplot)")
    if column not in df.columns:
        return JSONResponse({"error": "Columna no encontrada"}, status_code=400)
    plt.figure()
    sns.boxplot(x=df[column].dropna())
    plt.title(f"Boxplot de {column}")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (boxplot)")
    return {"img": img_base64}

@app.get("/api/nulls")
def nulls():
    df = get_df()
    nulls = df.isnull().sum().to_dict()
    return nulls

@app.get("/api/eda_text")
def eda_text():
    texto = (
        "Este dashboard muestra el análisis exploratorio de datos (EDA) del dataset de CS:GO. "
        "Incluye resumen de datos, estadísticas descriptivas, análisis de correlación, gráficos de barras y boxplot, "
        "así como el análisis de valores nulos. Puedes seleccionar columnas para visualizar diferentes aspectos del dataset."
    )
    return {"text": texto}

@app.get("/api/data_preparation_text")
def data_preparation_text():
    texto = (
        "CONTEXTO CASO\n\n"
        "Valve, los ha contactado como equipo de análisis de datos y modelado de Machine Learning para analizar y realizar modelos predictivos sobre los datos.\n\n"
        "En cada partida de Counter Strike: GO dos equipos de 5 jugadores (denominados terroristas y contra-terroristas) se enfrentan.\n\n"
        "El objetivo del equipo terrorista es plantar una bomba con timer de 45 segundos en uno de dos sitios específicos dentro de un mapa. Por otro lado, el objetivo del equipo contra-terrorista es evitar que la bomba sea plantada o desactivarla antes de que esta explote cuando ya ha sido plantada. Los datos a utilizar corresponden a sobre 7000 partidas del juego (con un máximo de 10 jugadores c/u)\n\n"
        "Los datos han sido extraídos de replays, los cuales son archivos propietarios con la información de cada una de las acciones realizadas por cada jugador dentro de una partida. Los replays han sido extraídos de la red utilizando un scrapper y pre-procesados utilizando un script.\n\n"
        "En este caso, la data corresponde a un archivo CSV con 79.157 filas, cada una correspondiente a un jugador dentro de una partida. El archivo contiene 29 columnas correspondientes a variables que describen las acciones del jugador dentro del juego."
    )
    return {"text": texto}

@app.get("/api/weapon_usage")
def weapon_usage():
    print("Entrando a weapon_usage")
    df = get_df()
    print("CSV cargado")
    armas = ['PrimaryAssaultRifle', 'PrimarySniperRifle', 'PrimaryHeavy', 'PrimarySMG', 'PrimaryPistol']
    uso_armas = df[armas].sum().sort_values(ascending=False)
    # Gráfico
    plt.figure(figsize=(8,6))
    uso_armas.plot(kind='bar')
    plt.title('Popularidad de tipos de armas')
    plt.ylabel('Cantidad de veces usada')
    plt.xlabel('Tipo de arma')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado")
    return {"table": uso_armas.to_dict(), "img": img_base64}

@app.get("/api/weapon_winrate")
def weapon_winrate():
    print("Entrando a weapon_winrate")
    df = get_df()
    print("CSV cargado (winrate)")
    df['UsaAssaultRifle'] = (df['PrimaryAssaultRifle'] > 0).astype(int)
    df['UsaSniperRifle'] = (df['PrimarySniperRifle'] > 0).astype(int)
    df['UsaHeavy'] = (df['PrimaryHeavy'] > 0).astype(int)
    df['UsaSMG'] = (df['PrimarySMG'] > 0).astype(int)
    df['UsaPistol'] = (df['PrimaryPistol'] > 0).astype(int)
    winrates = {
        'AssaultRifle': df[df['UsaAssaultRifle'] == 1]['MatchWinner'].mean(),
        'SniperRifle': df[df['UsaSniperRifle'] == 1]['MatchWinner'].mean(),
        'Heavy': df[df['UsaHeavy'] == 1]['MatchWinner'].mean(),
        'SMG': df[df['UsaSMG'] == 1]['MatchWinner'].mean(),
        'Pistol': df[df['UsaPistol'] == 1]['MatchWinner'].mean(),
    }
    # Gráfico
    plt.figure(figsize=(8,6))
    plt.bar(list(winrates.keys()), [float(v) for v in winrates.values()])
    plt.title('Tasa de victorias según tipo de arma usada')
    plt.ylabel('Porcentaje de victorias')
    plt.xlabel('Tipo de arma')
    plt.ylim(0,1)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (winrate)")
    return {"table": winrates, "img": img_base64}

@app.get("/api/regresion_dinero")
def regresion_dinero():
    print("Entrando a regresion_dinero")
    import io, base64
    import numpy as np
    from sklearn.linear_model import LinearRegression
    df = get_df()
    print("CSV cargado (regresion)")
    # Ajusta los nombres de columna según tu CSV
    X = df["RoundStartingEquipmentValue"].to_numpy().reshape(-1, 1)
    y = (df["RoundWinner"] == True) | (df["RoundWinner"] == 'True')
    y = y.astype(int)
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    # Usar objetos fig, ax para evitar errores de matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(X, y, color='blue', alpha=0.3, label='Datos reales')
    ax.plot(X, y_pred, color='red', label='Regresión lineal')
    ax.set_title('Dinero gastado vs Probabilidad de ganar')
    ax.set_xlabel('Dinero gastado')
    ax.set_ylabel('Probabilidad de ganar')
    ax.legend()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode()
    print("Procesamiento terminado (regresion)")
    return {
        "coef": float(model.coef_[0]),
        "intercept": float(model.intercept_),
        "img": img_base64
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 