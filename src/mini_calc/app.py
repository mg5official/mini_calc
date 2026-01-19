# ===================================================================
# Mini-Rechner Anwendung mit Tkinter (optisch verbessert)
# ===================================================================
# Diese Anwendung erstellt einen einfachen grafischen Taschenrechner,
# der die vier Grundrechenarten (Addition, Subtraktion, Multiplikation,
# Division) unterstützt.
#
# Optik-Verbesserungen gegenüber der Basisversion:
# - Mehr Abstand (Padding) und ein Rahmen-Container
# - Überschriften ("Zahl A", "Zahl B", "Ergebnis")
# - Ergebnisfeld wie “Display” (sunken/relief, größere Schrift)
# - Buttons mit einheitlicher Größe und farblicher Hervorhebung
# - Clear-Button + Tastatur-Shortcuts (Enter, Escape)
# - Dezimal-Komma wird akzeptiert ("," wird zu ".")
# ===================================================================

import tkinter as tk


# ===================================================================
# Funktionen
# ===================================================================

def calculate(op: str) -> None:
    """
    Führt eine Berechnung basierend auf dem Operator 'op' aus und schreibt
    das Ergebnis in die Tkinter-Variable 'result'.

    Parameter
    ---------
    op : str
        Der Operator als String:
        '+'  Addition
        '-'  Subtraktion
        '*'  Multiplikation
        '/'  Division

    Fehlerfälle
    ----------
    - Ungültige Eingaben (z.B. Buchstaben): Ergebnis = "Ungültige Eingabe"
    - Division durch 0: Ergebnis = "Fehler: ÷0"
    """
    try:
        # Werte aus den Eingabefeldern holen.
        # replace(",", ".") erlaubt Eingaben wie "3,14" (deutsches Komma).
        a = float(entry_a.get().replace(",", "."))
        b = float(entry_b.get().replace(",", "."))

        # Operator auswerten und Ergebnis berechnen
        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            # Division: Sonderfall b == 0 abfangen
            res = "Fehler: ÷0" if b == 0 else a / b
        else:
            # Falls aus irgendeinem Grund ein unbekannter Operator ankommt
            res = "Unbekannter Operator"

        # Ergebnis (res) in die StringVar schreiben -> Label aktualisiert sich automatisch
        result.set(res)

    except ValueError:
        # Wird ausgelöst, wenn float(...) nicht klappt (z.B. leeres Feld oder Text)
        result.set("Ungültige Eingabe")


def clear() -> None:
    """
    Löscht beide Eingabefelder und das Ergebnisfeld.
    Setzt den Fokus wieder auf das erste Eingabefeld.
    """
    entry_a.delete(0, tk.END)   # Inhalt von entry_a komplett löschen
    entry_b.delete(0, tk.END)   # Inhalt von entry_b komplett löschen
    result.set("")              # Ergebnisanzeige leeren
    entry_a.focus_set()         # Cursor/Fokus zurück in entry_a


# ===================================================================
# Hauptfenster erstellen
# ===================================================================

root = tk.Tk()                      # Root-Fenster erzeugen
root.title("Mini-Rechner")          # Titel in der Fensterleiste
root.resizable(False, False)        # Fenstergröße fixieren (kein Ziehen/Resizing)

# Etwas „Luft“ außen herum, damit es nicht so gequetscht aussieht
root.configure(padx=16, pady=16)


# ===================================================================
# Container-Frame (Rahmen) für ein „App“-Look
# ===================================================================
# Ein Frame ist ein Container, in dem andere Widgets liegen.
# Hier nutzen wir ihn zusätzlich als optischen Rahmen (bd + relief).
frame = tk.Frame(
    root,
    padx=14, pady=14,     # Innenabstand im Frame
    bd=2,                 # Randstärke
    relief="groove"       # Rahmendesign
)
frame.grid(row=0, column=0)         # Frame ins Root-Fenster setzen


# ===================================================================
# Fonts / Design-Grundlagen
# ===================================================================
# Einheitliche Schrift für bessere Lesbarkeit (Windows: Segoe UI)
FONT_MAIN = ("Segoe UI", 12)        # Standardtext
FONT_BIG  = ("Segoe UI", 14, "bold")# Größer/fett, z.B. für Ergebnis & Operatoren

# StringVar: Tkinter Variable, die Widgets automatisch aktualisieren kann
# -> Wenn result.set(...) aufgerufen wird, aktualisiert sich das Label.
result = tk.StringVar(value="")


# ===================================================================
# Eingabebereich (Zahl A / Zahl B)
# ===================================================================

# Labels über den Eingabefeldern
tk.Label(frame, text="Zahl A", font=FONT_MAIN).grid(row=0, column=0, sticky="w")
tk.Label(frame, text="Zahl B", font=FONT_MAIN).grid(row=0, column=1, sticky="w")

# Entry-Felder (Eingabefelder)
# justify="right" sorgt für rechtsbündige Eingabe wie bei Taschenrechnern.
entry_a = tk.Entry(frame, font=FONT_MAIN, width=14, justify="right")
entry_b = tk.Entry(frame, font=FONT_MAIN, width=14, justify="right")

# Positionierung (Grid)
entry_a.grid(row=1, column=0, padx=6, pady=(2, 10))
entry_b.grid(row=1, column=1, padx=6, pady=(2, 10))


# ===================================================================
# Ergebnisanzeige
# ===================================================================

# Überschrift "Ergebnis"
tk.Label(frame, text="Ergebnis", font=FONT_MAIN).grid(
    row=2, column=0, columnspan=2, sticky="w"
)

# Ergebnis-Label als „Display“:
# - relief="sunken" gibt den Look eines eingedrückten Feldes
# - anchor="e" (east) richtet den Text rechts aus
# - width ist hier in Zeichen (nicht Pixel)
result_label = tk.Label(
    frame,
    textvariable=result,  # zeigt den Inhalt von result an
    font=FONT_BIG,
    anchor="e",
    width=30,
    bd=2,
    relief="sunken",
    padx=10,
    pady=8
)
result_label.grid(row=3, column=0, columnspan=2, pady=(2, 12), sticky="we")


# ===================================================================
# Buttons (Operatoren + Clear)
# ===================================================================

# Ein extra Frame für die Operator-Buttons (bessere Struktur)
btn_frame = tk.Frame(frame)
btn_frame.grid(row=4, column=0, columnspan=2, sticky="we")

# Einheitliche Größe der Operator-Buttons
BTN_W, BTN_H = 6, 2


def make_btn(text: str, op: str | None = None, bg: str | None = None) -> tk.Button:
    """
    Hilfsfunktion, um Buttons einheitlich zu erstellen.

    Parameter
    ---------
    text : str
        Text auf dem Button (z.B. "+", "×", "÷")
    op : str | None
        Wenn gesetzt: Operator, der an calculate(op) übergeben wird.
        Wenn None: Button führt clear() aus.
    bg : str | None
        Hintergrundfarbe (Hex-Farbcode), um Buttons optisch zu unterscheiden.

    Rückgabe
    --------
    tk.Button
        Der fertig konfigurierte Button.
    """
    # Wenn op gesetzt ist: Klick ruft calculate(op) auf, sonst clear()
    cmd = (lambda: calculate(op)) if op else clear

    return tk.Button(
        btn_frame,
        text=text,
        font=FONT_BIG,
        width=BTN_W,
        height=BTN_H,
        bd=0,                 # ohne 3D-Rand (moderner)
        padx=6,
        pady=2,
        command=cmd,
        bg=bg if bg else None,
        activebackground=bg if bg else None
    )


# Operator-Buttons platzieren (Grid in btn_frame)
# Achtung: Für Multiplikation/Division zeigen wir schöne Zeichen (×, ÷),
# aber übergeben intern '*' bzw. '/' an calculate().
make_btn("+", "+", bg="#d9ead3").grid(row=0, column=0, padx=5, pady=5)  # grünlich
make_btn("-", "-", bg="#fce5cd").grid(row=0, column=1, padx=5, pady=5)  # orange
make_btn("×", "*", bg="#cfe2f3").grid(row=0, column=2, padx=5, pady=5)  # blau
make_btn("÷", "/", bg="#ead1dc").grid(row=0, column=3, padx=5, pady=5)  # rosa

# Clear-Button über die volle Breite (columnspan=2)
tk.Button(
    frame,
    text="Clear (Esc)",
    font=FONT_MAIN,
    command=clear
).grid(row=5, column=0, columnspan=2, sticky="we", pady=(6, 0))


# ===================================================================
# Tastatur-Shortcuts
# ===================================================================
# Enter rechnet standardmäßig PLUS (kannst du auch ändern)
# Escape leert die Felder
root.bind("<Return>", lambda e: calculate("+"))
root.bind("<Escape>", lambda e: clear())


# Start: Fokus direkt ins erste Feld, damit man sofort tippen kann
entry_a.focus_set()

# Tkinter Event-Loop starten (Fenster bleibt offen, reagiert auf Klicks/Eingaben)
root.mainloop()
