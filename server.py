from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import re
from datetime import datetime

app = Flask(__name__)

def init():
    conn = sqlite3.connect("gastos.db")
    conn.execute("CREATE TABLE IF NOT EXISTS gastos (categoria TEXT, valor REAL, data TEXT)")
    conn.commit()
    conn.close()

init()

def salvar(cat, valor):
    conn = sqlite3.connect("gastos.db")
    conn.execute("INSERT INTO gastos VALUES (?,?,?)", (cat, valor, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def total(cat):
    conn = sqlite3.connect("gastos.db")
    r = conn.execute("SELECT SUM(valor) FROM gastos WHERE categoria=?", (cat,))
    t = r.fetchone()[0]
    conn.close()
    return t or 0


@app.route("/bot", methods=["POST"])
def bot():
    msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()

    categorias = ["mercado","uber","farmacia","aluguel","luz","agua","internet"]

    numero = re.search(r'\d+[.,]?\d*', msg)

    if numero:
        valor = float(numero.group().replace(",","."))
        for c in categorias:
            if c in msg:
                salvar(c, valor)
                resp.message(f"✅ Salvo: {c} R$ {valor:.2f}")
                return str(resp)

    if "quanto" in msg:
        for c in categorias:
            if c in msg:
                t = total(c)
                resp.message(f"💰 Total {c}: R$ {t:.2f}")
                return str(resp)

    resp.message("Envie: mercado 120 ou quanto mercado?")
    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
