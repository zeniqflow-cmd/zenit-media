import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

NAME = "2026-11-24_cedole_etf"

def src(im, t, dark=False):
    d = ImageDraw.Draw(im)
    d.text((80, H - 150), t, font=f("Inter-Regular.otf", 26), fill=(150, 160, 180) if dark else (140, 140, 140))
    return im

def cta(title, body, i, n):
    im, d, fg = frame(i, n, True)
    y = block(d, 80, 280, title, T, CREAM, 920, 1.15); y += 40
    y = block(d, 80, y, body, B, (200, 208, 220), 920); y += 60
    d.rounded_rectangle([80, y, W - 80, y + 110], radius=55, fill=GOLD)
    d.text((W // 2, y + 55), "Commenta ZEN per il regalo", font=BB, fill=NAVY, anchor="mm"); y += 135
    d.rounded_rectangle([80, y, W - 80, y + 110], radius=55, outline=GOLD, width=3)
    d.text((W // 2, y + 55), "Salva e segui @zeni_thdigital", font=BB, fill=CREAM, anchor="mm")
    return im

N = 8
s = []
s.append(src(slide_hook("Piazza Affari · 23 novembre",
    "Milano ha \"perso\" l'1,4% in un secondo. Nessuno ha perso un euro.",
    "Il trucco dei dividendi che quasi nessuno capisce. E perché decide quale ETF ti conviene.", 0, N),
    "Fonte: ANSA, 23/11/2026", True))
s.append(src(slide("Cosa è successo",
    "+0,65% in TV, ma la giornata era più forte",
    "Il FTSE MIB ha chiuso a 49.021 punti (+0,65%), spinto dal ritorno di Jensen Huang alla guida di Nvidia. Ma 11 società hanno staccato il dividendo, e questo da solo ha tolto all'indice circa l'1,4%.",
    1, N, box="Senza lo stacco, la giornata sarebbe stata intorno al +2% (stima)."),
    "Fonti: ANSA, 23/11/2026; Reuters e CNBC, 23/11/2026"))
s.append(slide("Il meccanismo",
    "Il dividendo non è un regalo",
    "Il giorno dello stacco il prezzo dell'azione scende più o meno dell'importo del dividendo. I soldi escono dall'azienda ed entrano nel tuo conto.",
    2, N, box="Prima: azione a 10 €\nDopo: 9,50 € + 0,50 € di dividendo\nTotale: sempre 10 €"))
s.append(src(slide("Poi arriva il Fisco",
    "Sul dividendo paghi subito il 26%",
    "Hai 1.000 azioni da 10 € (10.000 €) e ricevi 0,50 € ad azione: 500 € lordi. Il 26% va allo Stato, subito.",
    3, N, box="Incassi 370 €\nIl tuo patrimonio: 9.870 €\n(a parità di mercato)"),
    "Fonte: DPR 600/1973, art. 27 (ritenuta 26%)"))
s.append(src(slide("Negli ETF",
    "Accumulazione o distribuzione?",
    "ETF a distribuzione: ti gira le cedole, e ogni volta paghi il 26%.\nETF ad accumulazione: le reinveste dentro il fondo. Le tasse le paghi solo quando vendi.",
    4, N, box="Rimandare le tasse = più soldi che lavorano per te"),
    "Fonte: DPR 600/1973, art. 26-quinquies"))
s.append(slide("Esempio ipotetico",
    "20 anni, stessi soldi",
    "10.000 € investiti. Ipotesi: +7% l'anno, di cui 3% da cedole, reinvestite. Senza costi. Valori netti, dopo le tasse alla vendita.",
    5, N, box="Accumulazione: 31.236 €\nDistribuzione: 29.512 €\nDifferenza: 1.724 €"))
s.append(slide("Occhio all'indice",
    "Il FTSE MIB non conta le cedole",
    "È un indice \"di prezzo\": ogni stacco lo fa scendere. Per misurare il vero risultato si usa la versione Total Return, che reinveste i dividendi. Confronta il tuo ETF con quella, non col numero del TG.",
    6, N, box="Le cedole servono per vivere? Distribuzione.\nStai accumulando per il futuro? Guarda l'accumulazione."))
s.append(cta("Il dividendo non ti fa più ricco. Ti fa pagare le tasse prima.",
    "Ti mando la guida \"Cedole o accumulo?\" con il calcolo completo.", 7, N))

cap = open(os.path.join(os.path.dirname(__file__), "..", "posts", NAME, "didascalia.txt"), encoding="utf-8").read()
os.chdir(os.path.join(os.path.dirname(__file__), "..", "posts"))
save(NAME, s, cap)
