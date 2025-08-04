from flask import Flask, request, jsonify, render_template, send_file
import io
import pandas as pd
from data_processing import compute_idf

app = Flask(__name__)

# Carrega uma vez no startup
CSV_FILE = 'resultado_processado (2).csv'
DF = pd.read_csv(CSV_FILE, sep=',')

def get_fluxo_json(tipologia, city_state):
    df_filtrado = DF[(DF['tipologia'].str.lower() == tipologia.lower()) & 
                     (DF['city_state'].str.lower() == city_state.lower())]
    if df_filtrado.empty:
        return {'erro': 'Não encontrado'}

    # Mapear dias
    map_dias = {
        'segunda': 'dia_tipico', 'terça': 'dia_tipico', 'quarta': 'dia_tipico',
        'quinta': 'dia_tipico', 'sexta': 'dia_tipico',
        'sábado': 'sabado', 'domingo': 'domingo'
    }
    resultado = {'dia_tipico': [], 'sabado': [], 'domingo': []}
    for _, row in df_filtrado.iterrows():
        key = map_dias.get(row['dia'].strip().lower())
        if key:
            resultado[key].append({'hora': int(row['hora']), 'valor': float(row['fluxo'])})

    # Ordena por hora
    for key in resultado:
        resultado[key] = sorted(resultado[key], key=lambda x: x['hora'])
    return resultado

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    tipologia = request.args.get('tipologia')
    city_state = request.args.get('city_state')
    if not tipologia or not city_state:
        return jsonify({'erro': 'Parâmetros obrigatórios'}), 400
    data = compute_idf(DF, tipologia, city_state)
    if 'erro' in data:
        return jsonify(data), 404
    return jsonify(data)

@app.route('/download')
def download():
    tipologia = request.args.get('tipologia')
    city_state = request.args.get('city_state')
    data = get_fluxo_json(tipologia, city_state)
    if 'erro' in data:
        return "Dados não encontrados", 404
    txt = ""
    for key, valores in data.items():
        txt += f"=== {key.upper()} ===\n"
        for v in valores:
            txt += f"{str(v['hora']).zfill(2)}:00\t{v['valor']}\n"
        txt += "\n"
    return send_file(
        io.BytesIO(txt.encode('utf-8')),
        mimetype='text/plain',
        as_attachment=True,
        download_name=f"fluxo_{tipologia}_{city_state.replace('/','-')}.txt"
    )

if __name__ == '__main__':
    app.run(debug=True)