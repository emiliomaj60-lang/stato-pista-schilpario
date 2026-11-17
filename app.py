import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

app = Flask(__name__)

app.secret_key = "CENTRO_FONDO_SCHILPARIO_2026"

FILE_DATI = "dati.json"

PASSWORD_ADMIN = "s"

def carica_dati():

    with open(FILE_DATI, "r", encoding="utf-8") as f:
        dati = json.load(f)

    dati.setdefault("km", "0")
    dati.setdefault("temperatura_aria", "0")
    dati.setdefault("temperatura_neve", "0")

    dati.setdefault("ultima_battitura", "")
    dati.setdefault("data_battitura", "")

    dati.setdefault("modalita", "AUTO")
    dati.setdefault("ora_apertura", "08:30")
    dati.setdefault("ora_chiusura", "17:00")

    dati.setdefault("modalita_pattinaggio", "AUTO")
    dati.setdefault("ora_apertura_pattinaggio", "09:00")
    dati.setdefault("ora_chiusura_pattinaggio", "17:00")

    dati.setdefault("note", "")

    dati.setdefault("ticker", "")
    dati.setdefault("ticker_bg", "#f39c12")
    dati.setdefault("ticker_fg", "#000000")
    dati.setdefault("ticker_speed", "20")
    dati.setdefault("ticker_animazione", "NESSUNA")

    return dati


def salva_dati(dati):

    with open(FILE_DATI, "w", encoding="utf-8") as f:
        json.dump(
            dati,
            f,
            ensure_ascii=False,
            indent=4
        )
    print(
        "SALVATI:",
        dati["ora_apertura"],
        dati["ora_chiusura"],
        dati["modalita"]
    )

def stato_effettivo(dati):

    modalita = dati.get("modalita", "AUTO")

    if modalita == "FORZA_APERTA":
        return "APERTA"

    if modalita == "FORZA_CHIUSA":
        return "CHIUSA"

    try:

        apertura = datetime.strptime(
            dati.get("ora_apertura", "08:30"),
            "%H:%M"
        ).time()

        chiusura = datetime.strptime(
            dati.get("ora_chiusura", "17:00"),
            "%H:%M"
        ).time()

        ora_attuale = datetime.now(
            ZoneInfo("Europe/Rome")
        ).time()

        if apertura <= ora_attuale <= chiusura:
            return "APERTA"

        return "CHIUSA"

    except Exception as e:

        print("ERRORE ORARI:", e)

        return "CHIUSA"

def stato_pattinaggio(dati):

    modalita = dati.get(
        "modalita_pattinaggio",
        "AUTO"
    )

    if modalita == "FORZA_APERTA":
        return "APERTA"

    if modalita == "FORZA_CHIUSA":
        return "CHIUSA"

    try:

        apertura = datetime.strptime(
            dati.get(
                "ora_apertura_pattinaggio",
                "09:00"
            ),
            "%H:%M"
        ).time()

        chiusura = datetime.strptime(
            dati.get(
                "ora_chiusura_pattinaggio",
                "17:00"
            ),
            "%H:%M"
        ).time()

        ora_attuale = datetime.now(
            ZoneInfo("Europe/Rome")
        ).time()

        if apertura <= ora_attuale <= chiusura:
            return "APERTA"

        return "CHIUSA"

    except Exception as e:

        print(
            "ERRORE ORARI PATTINAGGIO:",
            e
        )

        return "CHIUSA"

@app.route("/")
def home():

    return redirect("/condizioni")


@app.route("/condizioni")
def condizioni():

    dati = carica_dati()

    dati["stato"] = stato_effettivo(dati)
    dati["stato_pattinaggio"] = stato_pattinaggio(dati)

    return render_template(
        "condizioni.html",
        dati=dati
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    errore = ""

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

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

        dati["modalita"] = request.form.get(
            "modalita",
            "AUTO"
        )

        dati["ora_apertura"] = request.form.get(
            "ora_apertura",
            "08:30"
        )

        dati["ora_chiusura"] = request.form.get(
            "ora_chiusura",
            "17:00"
        )

        dati["modalita_pattinaggio"] = request.form.get(
            "modalita_pattinaggio",
            "AUTO"
        )

        dati["ora_apertura_pattinaggio"] = request.form.get(
            "ora_apertura_pattinaggio",
            "09:00"
        )

        dati["ora_chiusura_pattinaggio"] = request.form.get(
            "ora_chiusura_pattinaggio",
            "17:00"
        )

        dati["km"] = request.form.get(
            "km",
            "0"
        )

        dati["temperatura_aria"] = request.form.get(
            "temperatura_aria",
            "0"
        )

        dati["temperatura_neve"] = request.form.get(
            "temperatura_neve",
            "0"
        )

        dati["ultima_battitura"] = request.form.get(
            "ultima_battitura",
            ""
        )

        dati["data_battitura"] = request.form.get(
            "data_battitura",
            ""
        )

        dati["note"] = request.form.get(
            "note",
            ""
        )

        dati["ticker"] = request.form.get(
            "ticker",
            ""
        )

        salva_dati(dati)

        dati["stato"] = stato_effettivo(dati)
        dati["stato_pattinaggio"] = stato_pattinaggio(dati)

        return render_template(
            "admin.html",
            dati=dati
        )

    dati["stato"] = stato_effettivo(dati)
    dati["stato_pattinaggio"] = stato_pattinaggio(dati)

    return render_template(
        "admin.html",
        dati=dati
    )

@app.route("/orari")
def orari():

    dati = carica_dati()

    dati["stato"] = stato_effettivo(dati)

    return render_template(
        "orari.html",
        dati=dati
    )

@app.route("/ticker")
def ticker():

    dati = carica_dati()

    return render_template(
        "ticker.html",
        dati=dati
    )

@app.route("/ticker_admin", methods=["GET","POST"])
def ticker_admin():

    if not session.get("logged"):
        return redirect("/login")

    dati = carica_dati()

    if request.method == "POST":

        dati["ticker"] = request.form.get(
            "ticker",
            ""
        )

        dati["ticker_bg"] = request.form.get(
            "ticker_bg",
            "#f39c12"
        )

        dati["ticker_fg"] = request.form.get(
            "ticker_fg",
            "#000000"
        )

        dati["ticker_speed"] = request.form.get(
            "ticker_speed",
            "20"
        )

        dati["ticker_animazione"] = request.form.get(
            "ticker_animazione",
            "NESSUNA"
        )
        salva_dati(dati)

        salva_dati(dati)

        return redirect("/admin")

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=True
    )