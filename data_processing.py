# data_processing.py
import pandas as pd
import numpy as np

# Mapeia nome do dia para categoria
DAY_GROUP = {
    'Monday':    'dia_tipico',
    'Tuesday':   'dia_tipico',
    'Wednesday': 'dia_tipico',
    'Thursday':  'dia_tipico',
    'Friday':    'dia_tipico',
    'Saturday':  'sabado',
    'Sunday':    'domingo',
}

def compute_idf(df, tipologia: str, city_state: str = None):
    """
    Retorna um dict com idf normalizado por hora para cada grupo de dia,
    filtrando por tipologia e, opcionalmente, city_state.
    """
    # 1) Filtrar
    q = (df['tipologia'] == tipologia)
    if city_state:
        q &= (df['city_state'] == city_state)
    sub = df[q]

    # 2) Para cada linha, extrair start/end e acumular em matriz 3×24
    #    3 grupos de dia: dia_tipico, sabado, domingo
    freq = {g: np.zeros(24, dtype=int) for g in DAY_GROUP.values()}

    for _, row in sub.iterrows():
        for day, interval in row[['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']].items():
            inicio, fim = interval.split(' - ')
            h0 = int(inicio.split(':')[0])
            h1 = int(fim.split(':')[0])
            grupo = DAY_GROUP[day]
            # Acrescenta 1 em todas as horas [h0, h1)
            freq[grupo][h0:h1] += 1

    # 3) Normalizar cada vetor em [0,1]
    idf = {
        grupo: [
            {'hora': h, 'valor': round((freq[grupo][h] / freq[grupo].max()) if freq[grupo].max()>0 else 0, 3)}
            for h in range(24)
        ]
        for grupo in freq
    }

    return idf