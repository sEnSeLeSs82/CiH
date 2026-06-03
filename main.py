# main.py

import os, sys, sqlite3

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
    print(" Bitte gib a für ausgabe oder e für Einname ein")
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
       
        print ("Es sind jetzt ", saldo, "€ im Saldo")
        print("beenden? y oder n eingeben")
        stay=(input(""))       
        
    elif auswahl=="e":
        
        print("Du hast Einnahme gewählt")
        
        haben = einnahme()
        saldo = (saldo + haben)
        
        print ("Es sind jetzt ", saldo, "€ im Saldo")
        
        print ("beenden? y oder n eingeben")
        stay=(input(""))
        
    else:
        print ("Auswahl nicht erkannt")
        print ("beenden? y oder n eingeben")
        stay=(input(""))

connection.close()