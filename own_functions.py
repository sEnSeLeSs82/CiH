# own_functions

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