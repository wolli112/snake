'''
Einfaches Snake Spiel
https://github.com/wolli112/snake

MIT License

Copyright (c) 2024 wolli112

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
__version__ = '0.1'
__author__ = 'wolli112'

import tkinter as tk
import random

# Fenster erstellen
fenster = tk.Tk()
fenster.title("Snake Spiel")
fenster.resizable(False, False)

# Spielfeld-Parameter
breite = 500
hoehe = 500
zellengroesse = 20

# Farben definieren
hintergrundfarbe = "black"
schlangenfarbe = "green"
essenfarbe = "red"

# Spielfeld erstellen
canvas = tk.Canvas(fenster, width=breite, height=hoehe, bg=hintergrundfarbe)
canvas.pack()

# Anfangswerte der Schlange
schlange = [(100, 100), (80, 100), (60, 100)]
richtung = "Rechts"

# Essen-Position
essen = None

# Punkte
punkte = 0

# Funktion zur Erstellung von Essen
def erstelle_essen():
    global essen
    x = random.randint(0, (breite // zellengroesse) - 1) * zellengroesse
    y = random.randint(0, (hoehe // zellengroesse) - 1) * zellengroesse
    essen = (x, y)

# Funktion zur Bewegung der Schlange
def bewege_schlange():
    global richtung, schlange, spiel_laeuft, essen, punkte
    kopf_x, kopf_y = schlange[0]

    # Neue Position des Kopfes
    if richtung == "Rechts":
        kopf_x += zellengroesse
    elif richtung == "Links":
        kopf_x -= zellengroesse
    elif richtung == "Oben":
        kopf_y -= zellengroesse
    elif richtung == "Unten":
        kopf_y += zellengroesse

    # Neue Position des Kopfes überprüfen
    neuer_kopf = (kopf_x, kopf_y)

    # Kollision prüfen
    if (kopf_x < 0 or kopf_x >= breite or
        kopf_y < 0 or kopf_y >= hoehe or
        neuer_kopf in schlange[1:]):
        spiel_laeuft = False
        canvas.create_text(breite//2, hoehe//2, text=f"Game Over\nPunkte: {punkte}", fill="white", font=("Arial", 24))
        return

    # Prüfen, ob die Schlange das Essen erreicht hat
    if neuer_kopf == essen:
        schlange.append(schlange[-1])  # Schlange verlängern
        punkte += 1
        erstelle_essen()  # Neues Essen erstellen
    else:
        schlange = [neuer_kopf] + schlange[:-1]

    # Schlange und Essen zeichnen
    zeichne_schlange()
    zeichne_essen()
    fenster.after(150, bewege_schlange) # Geschwindigkeit kleiner = schneller, größer = langsamer

# Funktion zur Steuerung
def aendere_richtung(neue_richtung):
    global richtung
    gegenteile = {"Links": "Rechts", "Rechts": "Links", "Oben": "Unten", "Unten": "Oben"}
    if neue_richtung != gegenteile[richtung]:
        richtung = neue_richtung

# Schlange zeichnen
def zeichne_schlange():
    canvas.delete("all")
    for segment in schlange:
        x, y = segment
        canvas.create_rectangle(x, y, x+zellengroesse, y+zellengroesse, fill=schlangenfarbe)

# Essen zeichnen
def zeichne_essen():
    if essen:
        x, y = essen
        canvas.create_oval(x, y, x+zellengroesse, y+zellengroesse, fill=essenfarbe)

# Steuerung mit Tastatur
def key_event(event):
    taste = event.keysym
    if taste == "Left":
        aendere_richtung("Links")
    elif taste == "Right":
        aendere_richtung("Rechts")
    elif taste == "Up":
        aendere_richtung("Oben")
    elif taste == "Down":
        aendere_richtung("Unten")

# Event binden
fenster.bind("<KeyPress>", key_event)

# Spiel starten
spiel_laeuft = True
erstelle_essen()
zeichne_schlange()
zeichne_essen()
bewege_schlange()

# Hauptschleife starten
fenster.mainloop()