# teste de api
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def carregar_operadoras():
    df = pd.read_csv("Operadoras_Ativas.csv", encoding="utf-8")
    return df

@app.route("/buscar_operadora", methods=["GET"])
def buscar_operadora():
    termo = request.args.get("termo", "").lower()
    df = carregar_operadoras()
    
    resultados = df[df.apply(lambda row: termo in row.astype(str).str.lower().to_string(), axis=1)]
    
    return jsonify(resultados.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
