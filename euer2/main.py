from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional
import sqlite3, os

app = FastAPI()

# Session-Middleware – Secret und Passwort aus Umgebungsvariablen
SESSION_SECRET = os.environ.get("SESSION_SECRET", "bitte-aendern-geheim")
APP_PASSWORD   = os.environ.get("APP_PASSWORD",   "geheim")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

templates = Jinja2Templates(directory="templates")
DB = os.environ.get("DB_PATH", "euer.db")

# ── Datenbank ────────────────────────────────────────────────────────────────

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS buchungen (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            datum        TEXT    NOT NULL,
            typ          TEXT    NOT NULL CHECK(typ IN ('einnahme','ausgabe')),
            beschreibung TEXT    NOT NULL,
            stunden      REAL,
            stundensatz  REAL,
            brutto       REAL,
            mwst_satz    REAL,
            netto        REAL,
            betrag       REAL    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS einstellungen (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        INSERT OR IGNORE INTO einstellungen VALUES ('stundensatz','20.00');
        """)

init()

# ── Auth ─────────────────────────────────────────────────────────────────────

def logged_in(request: Request) -> bool:
    return request.session.get("auth") == True

def require_login(request: Request):
    if not logged_in(request):
        return RedirectResponse("/login", status_code=303)
    return None

# ── Hilfsfunktionen ──────────────────────────────────────────────────────────

def get_stundensatz() -> float:
    with db() as c:
        r = c.execute("SELECT value FROM einstellungen WHERE key='stundensatz'").fetchone()
        return float(r["value"]) if r else 20.0

def set_stundensatz(val: float):
    with db() as c:
        c.execute("INSERT OR REPLACE INTO einstellungen VALUES ('stundensatz',?)", (str(val),))

def get_buchungen(jahr: int):
    with db() as c:
        return c.execute(
            "SELECT * FROM buchungen WHERE strftime('%Y',datum)=? ORDER BY datum DESC, id DESC",
            (str(jahr),)
        ).fetchall()

def get_saldo(jahr: int):
    with db() as c:
        r = c.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN typ='einnahme' THEN betrag ELSE 0 END),0) AS einnahmen,
                COALESCE(SUM(CASE WHEN typ='ausgabe'  THEN betrag ELSE 0 END),0) AS ausgaben
            FROM buchungen WHERE strftime('%Y',datum)=?
        """, (str(jahr),)).fetchone()
        return dict(r)

# ── Login / Logout ────────────────────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, fehler: str = ""):
    if logged_in(request):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "fehler": fehler})

@app.post("/login")
async def login_post(request: Request, passwort: str = Form(...)):
    if passwort == APP_PASSWORD:
        request.session["auth"] = True
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("login.html",
        {"request": request, "fehler": "Falsches Passwort."})

@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

# ── Hauptseite ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, jahr: Optional[int] = None):
    redir = require_login(request)
    if redir: return redir

    from datetime import date
    heute = date.today()
    jahr = jahr or heute.year
    buchungen  = get_buchungen(jahr)
    saldo_data = get_saldo(jahr)
    saldo      = round(saldo_data["einnahmen"] - saldo_data["ausgaben"], 2)
    return templates.TemplateResponse("index.html", {
        "request":     request,
        "buchungen":   buchungen,
        "saldo":       saldo,
        "einnahmen":   round(saldo_data["einnahmen"], 2),
        "ausgaben":    round(saldo_data["ausgaben"],  2),
        "stundensatz": get_stundensatz(),
        "jahr":        jahr,
        "heute":       heute.isoformat(),
        "jahre":       list(range(heute.year + 1, heute.year - 3, -1)),
    })

# ── Buchen ────────────────────────────────────────────────────────────────────

@app.post("/buchen")
async def buchen(
    request:         Request,
    datum:           str            = Form(...),
    typ:             str            = Form(...),
    beschreibung:    str            = Form(...),
    einnahme_modus:  str            = Form("stunden"),
    stunden:         Optional[float] = Form(None),
    stundensatz:     Optional[float] = Form(None),
    einnahme_betrag: Optional[float] = Form(None),
    brutto:          Optional[float] = Form(None),
    mwst_satz:       Optional[float] = Form(None),
):
    redir = require_login(request)
    if redir: return redir

    if typ == "einnahme":
        if einnahme_modus == "euro":
            betrag = round(einnahme_betrag or 0.0, 2)
            with db() as c:
                c.execute(
                    "INSERT INTO buchungen (datum,typ,beschreibung,betrag) VALUES (?,?,?,?)",
                    (datum, typ, beschreibung, betrag))
        else:
            satz   = stundensatz or get_stundensatz()
            betrag = round((stunden or 0) * satz, 2)
            with db() as c:
                c.execute(
                    "INSERT INTO buchungen (datum,typ,beschreibung,stunden,stundensatz,betrag) VALUES (?,?,?,?,?,?)",
                    (datum, typ, beschreibung, stunden, satz, betrag))
    else:
        mwst   = mwst_satz if mwst_satz is not None else 0.19
        brutto = brutto or 0.0
        netto  = round(brutto / (1 + mwst), 2) if mwst > 0 else brutto
        with db() as c:
            c.execute(
                "INSERT INTO buchungen (datum,typ,beschreibung,brutto,mwst_satz,netto,betrag) VALUES (?,?,?,?,?,?,?)",
                (datum, typ, beschreibung, brutto, mwst, netto, netto))

    return RedirectResponse("/", status_code=303)

# ── Löschen ───────────────────────────────────────────────────────────────────

@app.post("/loeschen/{id}")
async def loeschen(id: int, request: Request):
    redir = require_login(request)
    if redir: return redir
    with db() as c:
        c.execute("DELETE FROM buchungen WHERE id=?", (id,))
    return RedirectResponse("/", status_code=303)

# ── Stundensatz ───────────────────────────────────────────────────────────────

@app.post("/stundensatz")
async def update_stundensatz(request: Request, stundensatz: float = Form(...)):
    redir = require_login(request)
    if redir: return redir
    set_stundensatz(stundensatz)
    return RedirectResponse("/", status_code=303)
