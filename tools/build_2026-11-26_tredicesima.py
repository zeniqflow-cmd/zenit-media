import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

def src(im, t, dark=False):
    d = ImageDraw.Draw(im)
    d.text((80, H - 150), t, font=f("Inter-Regular.otf", 26), fill=(150, 160, 180) if dark else (140, 140, 140))
    return im

# Esempio ipotetico: tredicesima netta 1.200 €, divisa in 3 parti da 400 €.
T13 = 1200; P = T13 // 3
r = 0.05
fv10 = 400 * ((1 + r) ** 10 - 1) / r   # 5.031,16
fv20 = 400 * ((1 + r) ** 20 - 1) / r   # 13.226,38

N = 8
s = []
s.append(src(slide_hook("Tredicesima · Black Friday",
    "Hai 1.200 € di tredicesima. Venerdì è Black Friday.",
    "Stessa tredicesima, due destini: dove finiscono i tuoi soldi a gennaio e tra 20 anni. Esempio ipotetico con i numeri.", 0, N),
    "Esempio didattico. Non è consulenza finanziaria.", True))
s.append(slide("Due destini",
    "Marco e Sara: stessi 1.200 €",
    "Marco al Black Friday spende tutto e aggiunge 600 € di acquisti in 3 rate \"compra ora, paga dopo\". Sara divide la tredicesima in 3 parti uguali.",
    1, N, box="Marco: tutto speso + 3 rate da 200 €\nSara: 400 € fondo emergenze,\n400 € PAC in ETF, 400 € per sé"))
s.append(slide("Gennaio",
    "Arriva l'imprevisto da 400 €",
    "Le gomme dell'auto, il dentista, la caldaia. Succede, di solito nel mese sbagliato.",
    2, N, box="Marco: 0 € da parte, 200 € di rata\ne un nuovo debito da 400 €.\nSara: paga con il fondo emergenze.\nIl suo PAC resta intatto."))
s.append(src(slide("Intanto in borsa",
    "Oggi Milano −1,81%",
    "Il 25/11 il FTSE MIB ha chiuso a 47.249 punti. Pesano il tech legato all'intelligenza artificiale, i nuovi dazi proposti dagli USA e l'attesa di un rialzo dei tassi della Fed. Spread BTP-Bund a circa 112 punti.",
    3, N, box="Per questo il fondo emergenze\nnon va in borsa: ti servirebbe\nproprio in un giorno così."),
    "Fonti: ANSA 25/11/2026 ore 17:40 e 18:09; Teleborsa"))
s.append(src(slide("Il concetto",
    "Paga prima te stesso",
    "Sara non investe \"quello che avanza\": mette da parte prima di spendere. Il tempo poi lavora per lei con l'interesse composto: i rendimenti producono altri rendimenti.",
    4, N, box="400 € ogni dicembre al 5% annuo:\n10 anni: circa 5.000 € (4.000 versati)\n20 anni: circa 13.200 € (8.000 versati)"),
    "Esempio ipotetico: rendimento costante, senza costi né tasse."))
s.append(slide("Le rate",
    "Le rate spendono la tredicesima di domani",
    "Dal 20/11 il \"compra ora, paga dopo\" è credito al consumo (d.lgs. 212/2025): più controlli, costi più chiari, 14 giorni per ripensarci.\n\nMa ogni rata è un pezzo di stipendio futuro già speso.",
    5, N))
s.append(slide("Cosa fare",
    "La tredicesima in 3 parti",
    "1. Fondo emergenze, sul conto: fino a 3-6 mesi di spese.\n2. PAC in ETF per obiettivi lontani, solo con soldi che non ti servono per anni.\n3. Una parte per te, pagata subito, senza rate.\nHai debiti costosi? Prima quelli.",
    6, N))

im, d, fg = frame(7, N, True)
y = block(d, 80, 280, "Stessi 1.200 €. A gennaio uno ha una rata, l'altra ha un piano.", T, CREAM, 920, 1.15); y += 50
y = block(d, 80, y, "Regalo: \"Tredicesima in 3 parti\" (PDF).", B, (200, 208, 220), 920); y += 60
for lab in ["Commenta ZEN per il regalo", "Salva e segui @zeni_thdigital"]:
    d.rounded_rectangle([80, y, W - 80, y + 100], radius=50, outline=GOLD, width=3)
    d.text((W // 2, y + 50), lab, font=BB, fill=CREAM, anchor="mm"); y += 125
s.append(im)

print(round(fv10, 2), round(fv20, 2))
cap = open(os.path.join(os.path.dirname(__file__), "..", "posts", "2026-11-26_tredicesima", "didascalia.txt"), encoding="utf-8").read()
os.chdir(os.path.join(os.path.dirname(__file__), "..", "posts"))
save("2026-11-26_tredicesima", s, cap)
