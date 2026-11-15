import json
from flask import Flask, render_template, request, redirect
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "s" # ******** password **********
}

app = Flask(__name__)

FILE_DATI = "dati.json"

def carica_dati():
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        return json.load(f)

def salva_dati(dati):
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

dati = {
    "stato": "APERTA",
    "km": "12",
    "note": "Condizioni ottime"
}

@app.route("/")
def display():
    return render_template(
        "display.html",
        dati=carica_dati()
    )

@app.route("/admin", methods=["GET", "POST"])
@auth.login_required
def admin():

    dati = carica_dati()

    if request.method == "POST":

        dati["stato"] = request.form["stato"]
        dati["km"] = request.form["km"]
        dati["note"] = request.form["note"]
        dati["temperatura_aria"] = request.form["temperatura_aria"]
        dati["temperatura_neve"] = request.form["temperatura_neve"]
        dati["ultima_battitura"] = request.form["ultima_battitura"]

        salva_dati(dati)

        return redirect("/admin")

    return render_template(
        "admin.html",
        dati=dati
    )

@auth.verify_password
def verify_password(username, password):
    print("LOGIN:", username)

    if username in users and users[username] == password:
        return username

@app.route("/condizioni")
def condizioni():
    dati = carica_dati()
    return render_template(
        "condizioni.html",
        dati=dati
    )

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )