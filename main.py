# main.py

import os, sys, sqlite3
import csv

if os.path.exists("CashAufTäsch.db"):
    print("Datenbank vorhanden")
    
    
if not os.path.exists("CashAufTäsch.db"):
    print("keine Datenbak vorhande")
    

connection = sqlite3.connect("CashAufTäsch.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS umsatz(
    id INTEGER PRIMARY KEY,
    name TEXT, 
    betrag REAL)"""
)

from own_functions import einnahme
from own_functions import ausgabe


saldo = 0
stay="n"



while stay=="n":
    print(" Bitte gib a für ausgabe, e für Einname oder u für die Ausgabe der Umsätze ein")
    auswahl = input("")
    print(auswahl)
    
    if auswahl=="a": 
        print("Du hast Ausgabe gewählt")
        print("Wofür War die Ausgabe?")
        
        grund_ausgabe = input("")
        name=grund_ausgabe
        soll = ausgabe()
        betrag = - soll
                
        cursor.execute("""
            INSERT INTO umsatz (name , betrag) VALUES (?, ?)
            """, (name, betrag))
        
        connection.commit()
        saldo = (saldo - soll)
        cursor.execute("SELECT SUM(betrag) FROM umsatz")
        result = cursor.fetchone()
        summe = round(result[0],2)
        
        print ("Es sind jetzt ", summe, "€ im Saldo")
        print("beenden? y oder n eingeben")
        stay=(input(""))       
        
    elif auswahl=="e":
        
        print("Du hast Einnahme gewählt")
        print("Datum oder Grund der Einnahme?")
        
        grund_einnahme = input("")
        name=grund_einnahme
        
        haben = einnahme()
        
        saldo = (saldo + haben)
        
        betrag=haben
        cursor.execute("""
            INSERT INTO umsatz (name , betrag) VALUES (?, ?)
            """, (name, betrag))
        
        connection.commit()
        
        cursor.execute("SELECT SUM(betrag) FROM umsatz")
        result = cursor.fetchone()
        summe = round(result[0],2)
        
        print ("Es sind jetzt ", summe, "€ im Saldo")
        
        print ("beenden? y oder n eingeben")
        stay=(input(""))
        
    elif auswahl=="u":
        
        # Verbindung zur Datenbank herstellen
    #connection = sqlite3.connect("CashAufTäsch.db")
        cursor = connection.cursor()

    # Daten aus der Tabelle auswählen
        cursor.execute("SELECT * FROM umsatz")
        rows = cursor.fetchall()

    # In CSV-Datei schreiben
        with open("ausgabe.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Optional: Header schreiben
            # writer.writerow([desc[0] for desc in cursor.description])
            writer.writerows(rows)
            
            connection.close()
        print ("beenden? y oder n eingeben")
        stay=(input(""))
        
    else:
        print ("Auswahl nicht erkannt")
        print ("beenden? y oder n eingeben")
        stay=(input(""))

"""
print("möchtensie die umsätze jetzt ausgeben - j oder n")
frage_druck = input("")

if frage_druck=="j":

    
        
else:
    print("ok dann nicht")
"""

