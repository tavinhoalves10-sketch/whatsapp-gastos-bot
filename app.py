from flask import Flask, request
import requests

app = Flask(__name__)

INSTANCE = "3EE8F08CED07C00AEEFECACE2FAC868C"
TOKEN = "082BB58DE500A73ED02F1488"

gastos = {}

def enviar(numero, texto):
    url = f"https://api.z-api.io/instances/{INSTANCE}/token/{TOKEN}/send-text"

    payload = {
        "phone": numero,
        "message": texto
    }

    requests.post(url, json=payload)


@app.route("/bot", methods=["POST"])
def bot():
    data = request.json

    numero = data["phone"]
    msg = data["text"]["message"].lower()

    partes = msg.split()

    # salvar gasto
    if len(partes) == 2 and partes[1].replace('.', '').isdigit():
        categoria = partes[0]
        valor = float(partes[1])

        gastos[categoria] = gastos.get(categoria, 0) + valor

        enviar(numero, f"✅ Salvo: {categoria} R$ {valor:.2f}")

    # consultar gasto
    elif msg.startswith("quanto"):
        categoria = partes[1]
        total = gastos.get(categoria, 0)

        enviar(numero, f"💰 Total {categoria}: R$ {total:.2f}")

    return "ok"


@app.route("/")
def home():
    return "BOT ONLINE"
