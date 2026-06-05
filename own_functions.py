<<<<<<< HEAD
# own_functions
=======
# own_functions.py
# Hilfsfunktionen für die CashAufTäsch-Anwendung

import sqlite3
import csv
import os
from decimal import Decimal, ROUND_HALF_UP

STUNDENSATZ = Decimal("20")   # Stundensatz in Euro – hier zentral änderbar
MWST_FAKTOR = Decimal("1.19") # 19% Mehrwertsteuer
DB_NAME = "CashAufTäsch.db"


# ─── Interne Hilfsfunktionen ──────────────────────────────────────────────────

def _runden(betrag):
    """Rundet einen Decimal-Betrag kaufmännisch auf 2 Dezimalstellen."""
    return betrag.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _betrag_einlesen(hinweis="Betrag (Punkt statt Komma): "):
    """
    Liest so lange einen Betrag ein,
    bis eine gültige positive Zahl eingegeben wird.
    Gibt den Betrag als Decimal zurück.
    """
    while True:
        try:
            betrag = Decimal(input(hinweis))
            if betrag <= 0:
                print("Bitte einen positiven Betrag eingeben.")
            else:
                return betrag
        except Exception:
            print("Ungültige Eingabe – bitte eine Zahl eingeben (Punkt statt Komma).")


def _auswahl_einlesen(optionen, hinweis):
    """
    Liest so lange eine Auswahl ein,
    bis eine der erlaubten Optionen eingegeben wird.
    Bleibt bei if/in, da match case keine dynamischen Listen prüfen kann.
    """
    while True:
        auswahl = input(hinweis).strip().lower()
        if auswahl in optionen:
            return auswahl
        print(f"Ungültige Eingabe – bitte eine der folgenden Optionen wählen: {', '.join(optionen)}")


# ─── Datenbankfunktionen ──────────────────────────────────────────────────────

def datenbank_initialisieren():
    """
    Prüft ob die Datenbank existiert, stellt die Verbindung her
    und legt die Tabelle an falls nötig.
    Gibt connection und cursor zurück.
    """
    if os.path.exists(DB_NAME):
        print("Datenbank vorhanden.")
    else:
        print("Keine Datenbank vorhanden – eine neue wird erstellt.")

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS umsatz (
            id     INTEGER PRIMARY KEY,
            name   TEXT,
            betrag REAL
        )
    """)
    connection.commit()
    return connection, cursor


def get_saldo(cursor):
    """Berechnet den aktuellen Saldo aus der Datenbank und gibt ihn kaufmännisch gerundet zurück."""
    cursor.execute("SELECT SUM(betrag) FROM umsatz")
    result = cursor.fetchone()[0]
    if result is None:
        return Decimal("0.00")
    return _runden(Decimal(str(result)))


def eintrag_speichern(connection, cursor, name, betrag):
    """Speichert einen Umsatz-Eintrag (Einnahme oder Ausgabe) in der Datenbank."""
    cursor.execute(
        "INSERT INTO umsatz (name, betrag) VALUES (?, ?)",
        (name, float(betrag))  # SQLite erwartet float, daher Konvertierung von Decimal
    )
    connection.commit()


def umsaetze_anzeigen_und_exportieren(connection):
    """Gibt alle Umsätze im Terminal aus und exportiert sie in eine CSV-Datei."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM umsatz")
    rows = cursor.fetchall()

    if not rows:
        print("Keine Umsätze vorhanden.")
        return

    print("\n── Alle Umsätze ──────────────────────────")
    for zeile in rows:
        betrag = _runden(Decimal(str(zeile[2])))
        print(f"  ID: {zeile[0]} | Name: {zeile[1]} | Betrag: {betrag} €")
    print("──────────────────────────────────────────\n")

    with open("ausgabe.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Betrag"])
        writer.writerows(rows)
    print("Umsätze wurden in 'ausgabe.csv' exportiert.")


# ─── Menü-Hilfsfunktionen ─────────────────────────────────────────────────────

def frage_beenden():
    """Fragt den Benutzer ob das Programm beendet werden soll. Gibt True zurück wenn ja."""
    while True:
        match input("Beenden? (y/n): ").strip().lower():
            case "y":
                return True
            case "n":
                return False
            case _:
                print("Bitte nur 'y' oder 'n' eingeben.")


# ─── Einnahmen & Ausgaben ─────────────────────────────────────────────────────
>>>>>>> 3946a2b (KI anpassungen)

def einnahme():
    """
    Fragt den Benutzer nach einer Einnahme.
    Unterscheidet zwischen Euro-Betrag (e) und Stunden-basierter Abrechnung (h).
    Gibt den berechneten Betrag als Decimal zurück.
    """
    print("\n── Einnahme ──────────────────────────────")
    typ = _auswahl_einlesen(
        optionen=("e", "h"),
        hinweis="Euro-Betrag (e) oder Stunden (h)? "
    )

    match typ:
        case "e":
            betrag = _runden(_betrag_einlesen("Euro-Betrag: "))
            print(f"  Einnahme: {betrag} €")
            return betrag
        case "h":
            stunden = _betrag_einlesen("Anzahl Stunden: ")
            betrag = _runden(stunden * STUNDENSATZ)
            print(f"  {stunden} Stunden × {STUNDENSATZ} €/h = {betrag} €")
            return betrag


def ausgabe():
    """
    Fragt den Benutzer nach einer Ausgabe.
    Unterscheidet zwischen Brutto-Betrag mit MwSt-Abzug (m) und ohne MwSt-Abzug (o).
    Gibt den Netto-Betrag als Decimal zurück.
    """
    print("\n── Ausgabe ───────────────────────────────")
    typ = _auswahl_einlesen(
        optionen=("m", "o"),
        hinweis="Mit MwSt-Abzug (m) oder ohne (o)? "
    )

    match typ:
        case "m":
            brutto = _betrag_einlesen("Brutto-Betrag: ")
            netto = _runden(brutto / MWST_FAKTOR)
            mwst = _runden(brutto - netto)
            print(f"  Brutto: {brutto} € | MwSt: {mwst} € | Netto: {netto} €")
            return netto
        case "o":
            betrag = _runden(_betrag_einlesen("Betrag: "))
            print(f"  Ausgabe: {betrag} €")
            return betrag