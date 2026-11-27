import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

def src(im, t, dark=False):
    d = ImageDraw.Draw(im)
    d.text((80, H - 150), t, font=f("Inter-Regular.otf", 26), fill=(150, 160, 180) if dark else (140, 140, 140))
    return im

def it(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

# Esempio ipotetico: 200.000 € a 25 anni, tasso fisso 3,5%, ammortamento alla francese, senza spese né assicurazioni.
P = 200000; r = 0.035 / 12; n = 300
R = P * r / (1 - (1 + r) ** -n)
rows = []; D = P
for k in range(1, n + 1):
    i = D * r; c = R - i; D -= c; rows.append((k, i, c, D))
paid60 = R * 60; res60 = rows[59][3]; cap60 = P - res60; int60 = paid60 - cap60
cross = next(k for k, i, c, _ in rows if c > i)
int_tot = R * n - P
# Rimborso parziale di 10.000 € dopo la rata 60, rata invariata
D = res60 - 10000; m = 0; ip = 0
while D > 0.005:
    i = D * r; c = min(R - i, D); ip += i; D -= c; m += 1
int_base = sum(x[1] for x in rows[60:])
saved = int_base - ip; months_less = 240 - m

assert round(R, 2) == 1001.25 and round(paid60) == 60075 and round(cap60) == 27359 and cross == 64
print(round(R, 2), round(paid60, 2), round(cap60, 2), round(int60, 2), round(res60, 2), cross, round(int_tot, 2), round(saved, 2), months_less)

N = 8
EX = "Esempio ipotetico: 200.000 €, 25 anni, fisso 3,5%, senza spese."
s = []
s.append(src(slide_hook("Mutuo · piano di ammortamento",
    f"Dopo 5 anni di mutuo hai pagato {it(paid60)} €. Quanto debito hai tolto?",
    "Prova a indovinare prima di scorrere. Mutuo di esempio: 200.000 € a 25 anni al 3,5% fisso.", 0, N),
    "Esempio didattico. Non è consulenza finanziaria.", True))
s.append(src(slide("La risposta",
    f"Solo {it(cap60)} €",
    f"60 rate da {it(R, 2)} €. Meno della metà è andata a ridurre il debito: il resto sono interessi.",
    1, N, box=f"Pagato in 5 anni: {it(paid60)} €\nInteressi: {it(int60)} €\nCapitale restituito: {it(cap60)} € (45,5%)\nDebito ancora da pagare: {it(res60)} €"),
    EX))
s.append(src(slide("Il concetto",
    "Rata uguale, dentro cambia tutto",
    "Nel mutuo \"alla francese\" (il più diffuso) la rata è fissa. Ma ogni mese paghi gli interessi sul debito che resta: all'inizio il debito è alto, quindi più di metà rata sono interessi.",
    2, N, box=f"Rata 1: {it(rows[0][1], 2)} € interessi,\n{it(rows[0][2], 2)} € capitale\nRata 300: {it(rows[-1][1], 2)} € interessi,\n{it(rows[-1][2], 2)} € capitale"),
    EX))
s.append(src(slide("Il sorpasso",
    f"Solo dalla rata {cross} il capitale supera gli interessi",
    "Cioè dopo 5 anni e 3 mesi. Interessi del mese = debito residuo × tasso annuo ÷ 12. Per questo i primi anni sono i più \"cari\".",
    3, N, box=f"In 25 anni paghi {it(R * n)} €:\n200.000 € di capitale\n+ {it(int_tot)} € di interessi"),
    EX))
s.append(src(slide("La leva",
    "10.000 € restituiti in anticipo",
    "Se dopo 5 anni rimborsi 10.000 € e tieni la stessa rata, tagli il debito su cui maturano gli interessi. Per i mutui casa delle persone fisiche non c'è penale (art. 120-ter TUB).",
    4, N, box=f"Interessi risparmiati: circa {it(round(saved, -1))} €\nMutuo finito {months_less} mesi prima"),
    "Stesso esempio ipotetico; calcolo con rata invariata."))
s.append(src(slide("Anticipare o investire?",
    "Rimborsare \"rende\" il tasso del mutuo",
    "Mutuo al 3,5%: rimborsare è un rendimento certo del 3,5%. Il 27/11 il BTP a 10 anni rendeva il 4,30% lordo (circa 3,76% netto) se tenuto a scadenza. La borsa può dare di più, senza certezze.",
    5, N, box="Prima il fondo emergenze.\nPoi confronta: tasso del mutuo\ncontro rendimento netto e rischio."),
    "Fonte: Teleborsa 27/11/2026 h 17:46. Tassa BTP 12,5%; senza detrazioni."))
s.append(src(slide("I numeri veri",
    "Fisso o variabile?",
    "A settembre 2026 il TAEG medio dei nuovi mutui casa era 4,05% (3,99% ad agosto). Solo il 16,9% dei nuovi mutui aveva il tasso variabile o fisso per al massimo 1 anno: oltre 8 su 10 bloccano il tasso per più di un anno.",
    6, N, box="Il 27/11 a Milano: FTSE MIB +1,89%\na 49.275,60 punti, spread BTP-Bund\na 104 punti base."),
    "Fonti: Banca d'Italia, Banche e moneta (10/11/2026); Teleborsa 27/11 h 17:46"))

im, d, fg = frame(7, N, True)
y = block(d, 80, 280, "Il tuo mutuo ha un piano di ammortamento. Leggilo.", T, CREAM, 920, 1.15); y += 50
y = block(d, 80, y, "Regalo: \"Leggi il tuo piano di ammortamento\" (PDF).", B, (200, 208, 220), 920); y += 60
for lab in ["Commenta ZEN per il regalo", "Salva e segui @zeni_thdigital"]:
    d.rounded_rectangle([80, y, W - 80, y + 100], radius=50, outline=GOLD, width=3)
    d.text((W // 2, y + 50), lab, font=BB, fill=CREAM, anchor="mm"); y += 125
s.append(im)

cap = open(os.path.join(os.path.dirname(__file__), "..", "posts", "2026-11-28_mutuo", "didascalia.txt"), encoding="utf-8").read()
os.chdir(os.path.join(os.path.dirname(__file__), "..", "posts"))
save("2026-11-28_mutuo", s, cap)
