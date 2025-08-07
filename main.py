from flask import Flask, request, jsonify, render_template, send_file
import io
import pandas as pd
from data_processing import compute_idf

app = Flask(__name__)

# Carrega uma vez no startup
CSV_FILE = 'resultado_processado (2).csv'
DF = pd.read_csv(CSV_FILE, sep=',')

# Tipologias fixas com label e value
TIPOLOGIAS_FIXAS = [
    {"label": "Escola Pública", "value": "school"},
    {"label": "Hospital", "value": "hospital"},
    {"label": "Cinema", "value": "movie_theater"},
    {"label": "Teatro", "value": "theater"},
    {"label": "Aeroporto", "value": "airport"},
    {"label": "Rodoviária", "value": "bus_station"},
    {"label": "Centro de Convenções", "value": "convention_center"},
    {"label": "Museu", "value": "museum"},
    {"label": "Hotel", "value": "hotel"},
    {"label": "Pousada", "value": "guesthouse"},
    {"label": "Shopping Center", "value": "shopping_center"},
    {"label": "Comércio", "value": "business"},
    {"label": "Varejo", "value": "retail"},
    {"label": "Loja", "value": "shop"},
    {"label": "Restaurante", "value": "restaurant"},
    {"label": "Universidade", "value": "university"},
    {"label": "Posto de Saúde", "value": "health_center"},
    {"label": "Processamento de Dados", "value": "data_center"},
]

CIDADES_FIXAS = [
    "São Paulo/SP", "Rio de Janeiro/RJ", "Belo Horizonte/MG", "Curitiba/PR",
    "Porto Alegre/RS", "Salvador/BA", "Brasília/DF", "Fortaleza/CE",
    "Recife/PE", "Manaus/AM", "Belém/PA", "Florianópolis/SC", "Goiânia/GO",
    "Vitória/ES", "Natal/RN", "Campo Grande/MS", "João Pessoa/PB",
    "Teresina/PI", "Palmas/TO", "Porto Velho/RO", "Macapá/AP", "Rio Branco/AC"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/options')
def options():
    return jsonify({
        "tipologias": TIPOLOGIAS_FIXAS,
        "cidades": CIDADES_FIXAS
    })

@app.route('/search')
def search():
    tipologia = request.args.get('tipologia')
    city_state = request.args.get('city_state')
    if not tipologia or not city_state:
        return jsonify({'erro': 'Parâmetros obrigatórios'}), 400
    try:
        data = compute_idf(DF, tipologia, city_state)
        if not data or all(len(d) == 0 for d in data.values()):
            return jsonify({'erro': 'Dados não encontrados'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/download')
def download():
    tipologia = request.args.get('tipologia')
    city_state = request.args.get('city_state')
    data = compute_idf(DF, tipologia, city_state)
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