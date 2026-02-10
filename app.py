from flask import Flask, request
import requests

app = Flask(__name__)

INSTANCE_ID = "3EE8F08CED07C00AEEFECACE2FAC868C"
TOKEN = "082BB58DE500A73ED02F1488"

@app.route("/bot", methods=["POST"])
def bot():
    data = request.json

    numero = data["phone"]
    mensagem = data["message"]

    resposta = f"Recebi: {mensagem}"

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text"

    payload = {
        "phone": numero,
        "message": resposta
    }

    requests.post(url, json=payload)

    return "ok"


app.run(host="0.0.0.0", port=10000)
