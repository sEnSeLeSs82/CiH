import sqlite3

connection = sqlite3.connect("CashAufTäsch.db")
cursor = connection.cursor()

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