# Projeto: Análise de Fluxo Horário de Pessoas por Tipologia

Este projeto fornece uma aplicação web para consultar, visualizar e baixar informações de movimentação de pessoas em diferentes **tipologias comerciais** (ex: supermercado, hospital, etc), separando a análise por **dias da semana** (dia típico, sábado, domingo) e por **horas**, tudo normalizado entre 0 e 1. A movimentação é baseada em dados históricos processados previamente.

## Funcionalidades

- Consulta por **tipologia** e (opcionalmente) cidade/estado.
- Visualização do fluxo horário por grupo de dias (dia típico, sábado, domingo).
- Geração de gráfico dinâmico do fluxo por hora.
- Download dos dados em formato `.txt`.
- API que retorna os dados prontos para uso em frontends JS.

## Estrutura dos Arquivos

- `main.py` — Backend Flask que serve as rotas e faz a orquestração.
- `data_processing.py` — Funções utilitárias para calcular a matriz IDF (intensity duration function) por hora/dia/tipologia.
- `resultado_processado.csv` — Base de dados consolidada, com horários de abertura por dia/tipologia/cidade.
- `index.html` — Frontend HTML/JS responsivo para interação do usuário.
- `requirements.txt` — Dependências do Python.

## Instalação:
1. **Acesso ao Repositório**
```sh
    - git clone ``` https://github.com/rayssa-freitas/DEO.git ```
    
    - cd ``` C:\Users\rayss\Downloads\DEO ```
```

2. **Criação do Ambiente Virtual**
```sh
    python -m venv venv
    source venv/bin/activate
```

3. **Instalação dos pacotes**
```sh
    pip install -r requirements.txt
```

4. **Executar a aplicação**
```sh
    python main.py
```

5. **Fazer download do CSV**:
   - Após rodar a busca, acesse no navegador:
     ```
     http://127.0.0.1:5000/download
     ```


 