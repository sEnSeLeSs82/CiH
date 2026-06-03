
import sqlite3

connection = sqlite3.connect("CashAufTäsch.db")
cursor = connection.cursor()
"""
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

for table in cursor.fetchall():
    print(table[0])

connection.close()




#sql = "SELECT * FROM umsatz"
#cursor.execute(sql)

    
#for dsatz in cursor:
#    print(dsatz[0], dsatz[1])
#connection.close()
"""


#cursor = CashAufTäsch.cursor()

# SQL-Abfrage für die Summe
cursor.execute("SELECT SUM(betrag) FROM umsatz")

# Ergebnis abrufen
# Da SUM() immer genau eine Zeile zurückgibt, ist fetchone() effizienter als fetchall()
result = cursor.fetchone()

# Das Ergebnis ist ein Tupel, z. B. (150.0), daher den Wert extrahieren
#if result:
summe = result[0]
#print(f"Die Summe beträgt: {summe}")
#else:
    #print("Keine Daten gefunden oder Spalte ist NULL.")
            
connection.close()

cursor.execute("SELECT SUM(betrag) FROM umsatz")
result = cursor.fetchone()
summe = result[0]