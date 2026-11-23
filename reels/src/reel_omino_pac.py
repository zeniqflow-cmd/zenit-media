# Reel "omino minimal": storia di un PAC ipotetico. Grafica originale, nessun audio (si aggiunge dall'app).
import sys,subprocess,math
from PIL import Image,ImageDraw,ImageFont
F="/usr/share/fonts/opentype/inter/"
def f(n,s): return ImageFont.truetype(F+n,s)
W,H,FPS=1080,1920,30
BG=(10,10,12); WH=(240,240,240); GR=(120,120,125); GOLD=(214,178,90); RED=(220,80,70); GREEN=(90,190,120)
K=f("Inter-SemiBold.otf",34); DAYF=f("InterDisplay-Bold.otf",120); BIG=f("InterDisplay-Bold.otf",84); MID=f("InterDisplay-Bold.otf",58)
SCR=f("InterDisplay-Bold.otf",92); SCRS=f("Inter-SemiBold.otf",30); SM=f("Inter-Regular.otf",28); BTN=f("InterDisplay-Bold.otf",44)
def ease(x): x=max(0.0,min(1.0,x)); return x*x*(3-2*x)
def lerp(a,b,t): return a+(b-a)*t
def eur(v): return f"{int(round(v)):,}".replace(",",".")+" €"
def figure(d,x,y,s=1.0,arm=0.0,turned=False):
    # omino originale: testa tonda + corpo a goccia, tutto bianco
    d.ellipse([x-38*s,y-200*s,x+38*s,y-124*s],fill=WH)
    d.rounded_rectangle([x-60*s,y-110*s,x+60*s,y+40*s],radius=int(55*s),fill=WH)
    if not turned:
        ax=x+60*s; ay=y-70*s; ex=ax+lerp(150,190,arm)*s; ey=ay+lerp(-10,-40,arm)*s
        d.line([ax,ay,ex,ey],fill=WH,width=int(26*s)); d.ellipse([ex-16*s,ey-16*s,ex+16*s,ey+16*s],fill=WH)
def desk(d,x,y):
    d.rectangle([x-40,y,x+520,y+14],fill=WH); d.rectangle([x+480,y+14,x+494,y+150],fill=WH)
    for k in range(0,1080,40): d.line([k,y+170,k+20,y+170],fill=GR,width=3)
def monitor(d,x,y,label,value,col,sub=None):
    d.rounded_rectangle([x,y,x+500,y+300],radius=22,outline=WH,width=8,fill=(18,18,22))
    d.rectangle([x+235,y+300,x+265,y+360],fill=WH)
    d.text((x+250,y+60),label,font=SCRS,fill=GR,anchor="mm")
    d.text((x+250,y+150),value,font=SCR,fill=col,anchor="mm")
    if sub: d.text((x+250,y+235),sub,font=SCRS,fill=GR,anchor="mm")
def battery(d,x,y,lvl,label):
    d.text((x,y-48),label,font=K,fill=WH)
    d.rounded_rectangle([x,y,x+200,y+80],radius=12,outline=WH,width=6); d.rectangle([x+200,y+25,x+215,y+55],fill=WH)
    n=max(0,min(5,round(lvl*5)))
    for i in range(n): d.rectangle([x+14+i*36,y+14,x+42+i*36,y+66],fill=GREEN if lvl>0.4 else RED)
def text_c(d,y,t,font,fill): d.text((W//2,y),t,font=font,fill=fill,anchor="mm")
def foot(d):
    d.text((W//2,1700),"Numeri ipotetici: 100 € al mese, percorso di prezzo inventato.",font=SM,fill=GR,anchor="mm")
    d.text((W//2,1740),"Non è consulenza finanziaria. @zeni_thdigital",font=SM,fill=GR,anchor="mm")
# scene: (inizio, fine)
S=[(0,3.2),(3.2,6.4),(6.4,10.4),(10.4,13.6),(13.6,17.6),(17.6,21.0)]
DUR=21.0
def frame(t):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    def sc(i): a,b=S[i]; return (t-a)/(b-a)
    fx,fy=290,1210
    if t<S[2][0]:
        i=0 if t<S[1][0] else 1; p=ease(sc(i)*1.6)
        day=[1,300][i]; dprev=[1,1][i]
        text_c(d,330,"GIORNI",K,GR); text_c(d,420,f"{int(lerp(dprev,day,p)):,}".replace(",","."),DAYF,WH)
        vals=[(100,100),(1100,1154)][i]; prev=[(0,0),(100,100)][i]
        v=lerp(prev[1],vals[1],p)
        monitor(d,470,640,"IL MIO PAC",eur(v),WH if i==0 else GREEN,f"versati {eur(lerp(prev[0],vals[0],p))}")
        desk(d,330,1210); figure(d,fx,fy,arm=0.5+0.5*math.sin(t*6))
        text_c(d,1480,["Inizio: 100 € al mese.","Tutto bene. Si sale."][i],MID,WH)
    elif t<S[3][0]:
        p=ease(sc(2)*1.5)
        text_c(d,330,"GIORNI",K,GR); text_c(d,420,f"{int(lerp(300,600,p)):,}".replace(",","."),DAYF,WH)
        v=lerp(1154,1830,p)
        drop = p>0.5
        monitor(d,470,640,"BORSA −20%" if drop else "IL MIO PAC",eur(v),RED if drop else WH,"versati 2.100 €")
        battery(d,90,620,lerp(1,0.2,p),"PAZIENZA")
        desk(d,330,1210); figure(d,fx,fy,arm=0)
        if drop: text_c(d,1480,"Il valore scende. Panico.",MID,RED)
    elif t<S[4][0]:
        p=sc(3)
        text_c(d,330,"GIORNO 601",K,GR); text_c(d,430,"Tutti vendono.",BIG,WH)
        # tasto VENDI lampeggiante
        on = int(t*4)%2==0
        d.rounded_rectangle([340,700,740,860],radius=80,fill=RED if on else (120,40,35))
        d.text((540,780),"VENDI",font=BTN,fill=WH,anchor="mm")
        figure(d,540,1250,arm=0,turned=p>0.55)
        if p>0.55: text_c(d,1480,"Lui no. Continua il PAC.",MID,GOLD)
    elif t<S[5][0]:
        p=ease(sc(4)*1.5)
        text_c(d,330,"GIORNI",K,GR); text_c(d,420,f"{int(lerp(600,1200,p)):,}".replace(",","."),DAYF,WH)
        monitor(d,470,640,"IL MIO PAC",eur(lerp(1830,4822,p)),GREEN,"versati 4.100 €")
        desk(d,330,1210); figure(d,fx,fy,arm=0.5+0.5*math.sin(t*6))
        if p>0.6:
            text_c(d,1440,"Chi ha venduto al giorno 600 ha incassato 1.830 €:",SCRS,GR)
            text_c(d,1500,"270 € meno di quanto aveva versato.",MID,RED)
    else:
        p=ease(sc(5)*2)
        text_c(d,620,"Nei cali il PAC",BIG,WH)
        text_c(d,720,"compra a sconto.",BIG,GOLD)
        text_c(d,880,"Il panico no.",MID,WH)
        d.rounded_rectangle([140,1040,940,1160],radius=60,outline=GOLD,width=4)
        d.text((540,1100),"Salva e segui @zeni_thdigital",font=f("Inter-SemiBold.otf",44),fill=WH,anchor="mm")
    foot(d)
    # barra di avanzamento
    d.rectangle([0,0,int(W*t/DUR),10],fill=GOLD)
    return im
out=sys.argv[1]
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart",out],stdin=subprocess.PIPE)
for i in range(int(DUR*FPS)): p.stdin.write(frame(i/FPS).tobytes())
p.stdin.close(); p.wait()
