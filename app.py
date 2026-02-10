from flask import Flask, request
import requests
import json

app = Flask(__name__)

INSTANCE_ID = "3EE8F08CED07C00AEEFECACE2FAC868C"
TOKEN = "082BB58DE500A73ED02F1488"

@app.route("/bot", methods=["POST"])
def bot():
    data = request.json
    print("Recebido:", data)

    numero = data.get("phone")
    texto = data.get("message")

    resposta = f"Recebi: {texto}"

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "phone": numero,
        "message": resposta
    }
    print("ENVIANDO PARA ZAPI...")
           
    r = requests.post(url, headers=headers, json=payload)

    print("Status envio:", r.status_code)
    print("Resposta API:", r.text)

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
