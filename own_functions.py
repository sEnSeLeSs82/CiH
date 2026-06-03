# own_functions

def einnahme():
    print("Was möchen Sie als Einnahme verbuchen?")
    print("Bite gib e für einen Euro Betrag oder h für Stunden ein")
    typ_einnahme=input()
    haben=0
    
    if typ_einnahme=="e": 
        print(typ_einnahme , "Du hast Euro gewählt")
        print("wie viel möchtest du verbuchen? Punkt anstelle von Komma")
        return float(input(""))
        
    elif typ_einnahme=="h":
        print(typ_einnahme , "Du hast Stunden gewählt")
        print("Wie viele Stunden möchtest du verbuchen? Punkt anstelle von Komma")
        return (float(input("")) *20)
        
    else:
        print(typ_einnahme , "Auswahl nicht erkannt")
        
def ausgabe():
    print("Was möchen Sie als AUSGABE verbuchen?")
    print("Bite gib m für für mit MwSt oder o für ohne MwSt Abzug ein")
    typ_ausgabe=input()
    soll=0
    
    if typ_ausgabe=="m": 
        print(typ_ausgabe , "Du hast mit MwSt Abzug gewählt")
        print("Bitte gib den Brutto Betrag ein")
        return (float(input(""))/1.19)
        
    elif typ_ausgabe=="o":
        print(typ_ausgabe , "Du hast ohne MwSt Abzug gewählt")
        print("Bitte gib den Brutto Betrag ein")
        return float(input(""))
        
    else:
        print(typ_ausgabe , "Auswahl nicht erkannt")