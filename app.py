import json
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)

app = Flask(__name__)

# Cambiala con una stringa lunga e segreta
app.secret_key = "CENTRO_FONDO_SCHILPARIO_2026"

FILE_DATI = "dati.json"

PASSWORD_ADMIN = "s"


def carica_dati():
    with open(FILE_DATI, "r", encoding="utf-8") as f:
        return json.load(f)


def salva_dati(dati):
    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)


@app.route("/")
def home():
    return redirect("/condizioni")


@app.route("/condizioni")
def condizioni():
    dati = carica_dati()
    return render_template(
        "condizioni.html",
        dati=dati
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    errore = ""

    if request.method == "POST":

        password = request.form.get("password", "")

        if password == PASSWORD_ADMIN:
            session["logged"] = True
            return redirect("/admin")

        errore = "Password errata"

    return render_template(
        "login.html",
        errore=errore
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if not session.get("logged"):
        return redirect("/login")

    dati = carica_dati()

    if request.method == "POST":

        dati["stato"] = request.form["stato"]
        dati["km"] = request.form["km"]
        dati["temperatura_aria"] = request.form["temperatura_aria"]
        dati["temperatura_neve"] = request.form["temperatura_neve"]
        dati["ultima_battitura"] = request.form["ultima_battitura"]
        dati["note"] = request.form["note"]

        salva_dati(dati)

        return redirect("/admin")

    return render_template(
        "admin.html",
        dati=dati
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )