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

    print("Recebi:", numero, mensagem)

    resposta = f"Você disse: {mensagem}"

    requests.post(
        f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}/send-text",
        json={
            "phone": numero,
            "message": resposta
        }
    )

    return "ok"

if __name__ == "__main__":
    app.run()
