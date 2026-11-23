# Genera un PDF "regalo" in stile Zenith da un file di testo semplice:
# riga 1 titolo, riga 2 sottotitolo, poi blocchi separati da riga vuota; "## " = intestazione, "- " = punto elenco.
import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
F="/usr/share/fonts/truetype/google-fonts/"
pdfmetrics.registerFont(TTFont("B",F+"Poppins-Bold.ttf")); pdfmetrics.registerFont(TTFont("R",F+"Poppins-Regular.ttf")); pdfmetrics.registerFont(TTFont("M",F+"Poppins-Medium.ttf"))
NAVY=(31/255,42/255,68/255); CREAM=(245/255,241/255,232/255); GOLD=(201/255,164/255,76/255); SAGE=(143/255,169/255,152/255)
src,out=sys.argv[1],sys.argv[2]; L=open(src,encoding="utf-8").read().split("\n")
W,H=A4; c=canvas.Canvas(out,pagesize=A4); M=56
def page_bg():
    c.setFillColorRGB(*CREAM); c.rect(0,0,W,H,fill=1,stroke=0); c.setFillColorRGB(*GOLD); c.rect(0,H-10,W,10,fill=1,stroke=0)
    c.setFillColorRGB(*NAVY); c.setFont("M",9); c.drawString(M,30,"Budget Zen · @zeni_thdigital · Materiale didattico, non è consulenza finanziaria.")
page_bg()
c.setFillColorRGB(*NAVY); c.rect(0,H-210,W,200,fill=1,stroke=0)
c.setFillColorRGB(*GOLD); c.setFont("M",11); c.drawString(M,H-70,"REGALO PER TE")
c.setFillColorRGB(*CREAM); c.setFont("B",26)
y=H-110
for l in simpleSplit(L[0],"B",26,W-2*M): c.drawString(M,y,l); y-=32
c.setFont("R",12); c.setFillColorRGB(0.8,0.83,0.88)
for l in simpleSplit(L[1],"R",12,W-2*M): c.drawString(M,y-4,l); y-=16
y=H-250
for raw in L[2:]:
    if y<80: c.showPage(); page_bg(); y=H-70
    if not raw.strip(): y-=8; continue
    if raw.startswith("## "):
        y-=10; c.setFillColorRGB(*GOLD); c.rect(M,y-4,4,20,fill=1,stroke=0); c.setFillColorRGB(*NAVY); c.setFont("B",15); c.drawString(M+14,y,raw[3:]); y-=26; continue
    bullet=raw.startswith("- "); t=raw[2:] if bullet else raw
    c.setFillColorRGB(*NAVY); c.setFont("R",11.5)
    lines=simpleSplit(t,"R",11.5,W-2*M-(18 if bullet else 0))
    for i,l in enumerate(lines):
        if bullet and i==0: c.setFillColorRGB(*GOLD); c.circle(M+4,y+4,2.6,fill=1,stroke=0); c.setFillColorRGB(*NAVY)
        c.drawString(M+(18 if bullet else 0),y,l); y-=16.5
c.save()
