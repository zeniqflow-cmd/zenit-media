import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

def src(im, t, dark=False):
    d = ImageDraw.Draw(im)
    d.text((80, H - 150), t, font=f("Inter-Regular.otf", 26), fill=(150, 160, 180) if dark else (140, 140, 140))
    return im

N = 8
s = []
s.append(src(slide_hook("Borsa · 24 novembre 2026",
    "1.000 € in una sola azione: −102 € in un giorno.",
    "STMicroelectronics ha perso il 10,21%. Il FTSE MIB l'1,84%. La differenza ha un nome: diversificazione.", 0, N),
    "Fonti: Borsa Italiana (Teleborsa), ANSA, 24/11/2026", True))
s.append(src(slide("Cosa è successo",
    "Milano la peggiore d'Europa",
    "Il tech è tornato sotto pressione per nuove incertezze sull'intelligenza artificiale e voci di nuovi dazi USA.",
    1, N, box="FTSE MIB −1,84%\nSTMicroelectronics −10,21%\nTechnoprobe −10,09%\nPrysmian −8,04%"),
    "Fonti: Borsa Italiana (Teleborsa), ANSA, 24/11/2026"))
s.append(slide("Stessi soldi, due scelte",
    "Una azione o tutto l'indice",
    "Chiusura del 23/11: avevi 1.000 €.\nChiusura del 24/11:",
    2, N, box="Tutto su STMicro: 897,90 €\nUn ETF sul FTSE MIB: circa 981,60 €\nDifferenza: circa 84 €"))
s.append(slide("Il concetto",
    "Ci sono due rischi diversi",
    "Rischio specifico: conti deludenti, una notizia, un settore in crisi. Colpisce poche aziende e lo riduci diversificando.\n\nRischio di mercato: scende tutta la borsa. Non si elimina: si gestisce con tempo e PAC.",
    3, N))
s.append(slide("La matematica",
    "Scendere è più facile che risalire",
    "Per tornare in pari dopo un calo serve un rialzo più grande del calo stesso.",
    4, N, box="−10%  →  serve +11,1%\n−30%  →  serve +42,9%\n−50%  →  serve +100%"))
s.append(slide("Esempio ipotetico",
    "Un titolo su 20 pesa poco",
    "Portafoglio di 10.000 € diviso in parti uguali su 20 azioni. Una fa −10,21%, le altre restano ferme.",
    5, N, box="Perdi 51 € (−0,5%),\nnon 1.021 € (−10,2%)."))
s.append(slide("Cosa fare",
    "La regola del nucleo",
    "1. Il cuore del PAC in ETF ampi: tante aziende, più settori e Paesi.\n2. Singole azioni? Solo una piccola parte, che accetti di vedere anche a −50%.\n3. Il rischio di mercato resta: non vendere nel panico.",
    6, N))

im, d, fg = frame(7, N, True)
y = block(d, 80, 280, "Una sola azione può perdere il 10% in un giorno. Tutto il mercato, molto più di rado.", T, CREAM, 920, 1.15); y += 50
y = block(d, 80, y, "Regalo: \"Il check-up della diversificazione\" (PDF).", B, (200, 208, 220), 920); y += 60
for lab in ["Commenta ZEN per il regalo", "Salva e segui @zeni_thdigital"]:
    d.rounded_rectangle([80, y, W - 80, y + 100], radius=50, outline=GOLD, width=3)
    d.text((W // 2, y + 50), lab, font=BB, fill=CREAM, anchor="mm"); y += 125
s.append(im)

cap = open(os.path.join(os.path.dirname(__file__), "..", "posts", "2026-11-25_diversificazione", "didascalia.txt"), encoding="utf-8").read()
os.chdir(os.path.join(os.path.dirname(__file__), "..", "posts"))
save("2026-11-25_diversificazione", s, cap)
