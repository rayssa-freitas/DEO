from flask import Flask, request, jsonify, render_template
import pandas as pd
from data_processing import compute_idf

app = Flask(__name__)

# Carrega uma vez no startup
DF = pd.read_csv('resultado_processado.csv', sep=',')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    tipologia   = request.args.get('tipologia')
    city_state  = request.args.get('city_state', None)
    if not tipologia:
        return jsonify({'error':'tipologia obrigatória'}), 400

    idf = compute_idf(DF, tipologia, city_state)
    return jsonify(idf)

if __name__ == '__main__':
    app.run(debug=True)