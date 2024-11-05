from flask import Flask, request, jsonify, send_file, redirect
from flasgger import Swagger, swag_from
import pandas as pd
from io import BytesIO

# Importando as funções do pipeline e do modelo
from model_service import model_predict
from pipeline_service import run_pipeline

app = Flask(__name__)
swagger = Swagger(app)  

@app.route('/upload-csv', methods=['POST'])
@swag_from({
    'summary': 'Faz o upload de um CSV, processa os dados e retorna as predições.',
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Arquivo CSV para upload.'
        }
    ],
    'responses': {
        200: {
            'description': 'Arquivo processado com sucesso.',
            'content': {
                'text/csv': {
                    'schema': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
        400: {
            'description': 'Erro no upload do arquivo.'
        },
        500: {
            'description': 'Erro interno no servidor.'
        }
    }
})
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nome de arquivo inválido"}), 400

    try:
        # Lendo o arquivo CSV
        df = pd.read_csv(file)

        # Passando dados pela pipeline
        df = run_pipeline(df)

        # Passando pelo modelo
        df = model_predict(df)

        # Salvando o resultado em um arquivo CSV 
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Retornando o CSV processado para download
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='predicted_output.csv')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return redirect('/apidocs')


if __name__ == '__main__':
    app.run(debug=True)
