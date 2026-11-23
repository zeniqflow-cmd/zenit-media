import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

def src(im, t):
    d = ImageDraw.Draw(im)
    d.text((80, H - 150), t, font=f("Inter-Regular.otf", 26), fill=(140, 140, 140))
    return im

def src_dark(im, t):
    d = ImageDraw.Draw(im)
    d.text((80, H - 150), t, font=f("Inter-Regular.otf", 26), fill=(150, 160, 180))
    return im

N = 8
s = []
s.append(src_dark(slide_hook("Mercati · novembre 2026",
    "Borsa sulle montagne russe. Vendo il mio PAC?",
    "Il 5 novembre il Nasdaq ha perso il 4,9% in un giorno. Oggi il tech è tornato a correre. Prima di toccare qualcosa, leggi qui.", 0, N),
    "Fonte: Milano Finanza, 5/11 e 23/11/2026"))
s.append(src(slide("È normale",
    "Succede quasi ogni anno",
    "Dal 1980 la borsa americana (S&P 500) ha avuto in media un calo del 14,2% in qualche momento dell'anno.",
    1, N, box="Eppure ha chiuso l'anno in positivo 33 volte su 44."),
    "Fonte: J.P. Morgan, Guide to the Markets (dati 1980-2023)"))
s.append(slide("Il trucco del PAC",
    "Quando scende, compri di più",
    "Con 100 € al mese, se la quota costa 10 € ne compri 10. Se scende a 8 €, con gli stessi 100 € ne compri 12,5.",
    2, N, box="+25% di quote con gli stessi soldi"))
s.append(slide("Esempio",
    "Giù e su: chi ci guadagna",
    "Investi 100 € al mese per 6 mesi. La quota parte da 10 €, scende a 9, 8, 8, 9 e torna a 10.",
    3, N, box="Hai messo 600 €.\nOra valgono 672 € (+12%),\nanche se il prezzo è tornato al punto di partenza."))
s.append(slide("L'errore",
    "Vendere rende vera la perdita",
    "Finché non vendi, la perdita è solo sulla carta. Se vendi adesso, la blocchi e rischi di perderti la risalita, che nessuno sa prevedere.",
    4, N))
s.append(src(slide("In Italia",
    "La trappola fiscale degli ETF",
    "Se vendi un ETF in perdita, quella perdita non si può compensare con i guadagni futuri di altri ETF.",
    5, N, box="Vale solo contro guadagni su azioni, obbligazioni o ETC, entro 4 anni."),
    "Fonte: TUIR, artt. 44, 67 e 68"))
s.append(slide("Cosa fare",
    "La regola dei 3 cassetti",
    "1. Emergenze: 3-6 mesi di spese sul conto, fuori dalla borsa.\n2. Soldi che servono entro 3-5 anni (es. anticipo casa): niente azioni.\n3. Il resto, nel PAC: lascialo correre.",
    6, N))
s.append(slide_cta("Il PAC non teme i ribassi. Li usa.",
    "Salva e segui @zeni_thdigital per non farti prendere dal panico la prossima volta.", 7, N))

cap = open(os.path.join(os.path.dirname(__file__), "..", "posts", "2026-11-23_borsa_pac", "didascalia.txt"), encoding="utf-8").read()
os.chdir(os.path.join(os.path.dirname(__file__), "..", "posts"))
save("2026-11-23_borsa_pac", s, cap)
