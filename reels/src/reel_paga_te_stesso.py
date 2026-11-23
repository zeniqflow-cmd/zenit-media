# Reel omino + voce (Kokoro im_nicola, Apache 2.0) + base musicale fornita da Gianni.
import sys,subprocess,math
from PIL import Image,ImageDraw,ImageFont
F="/usr/share/fonts/opentype/inter/"
def f(n,s): return ImageFont.truetype(F+n,s)
W,H,FPS=1080,1920,30; DUR=31.0
BG=(10,10,12); WH=(240,240,240); GR=(120,120,125); GOLD=(214,178,90); RED=(220,80,70); GREEN=(90,190,120)
K=f("Inter-SemiBold.otf",34); DAYF=f("InterDisplay-Bold.otf",110); BIG=f("InterDisplay-Bold.otf",92); MID=f("InterDisplay-Bold.otf",60)
SCR=f("InterDisplay-Bold.otf",92); SCRS=f("Inter-SemiBold.otf",30); SM=f("Inter-Regular.otf",28); SUB=f("Inter-SemiBold.otf",46)
T=eval(open(sys.argv[2]).read())
LINES=["Marco, 22 anni. Primo stipendio: 1.400 €.","Giorno 30. Sul conto: zero.","Succede ogni mese. Non guadagna poco: non tiene niente.","Poi cambia una sola regola.","Il giorno dello stipendio, il 10% va subito su un conto a parte.","140 € al mese. Dopo un anno: 1.680 €.","Non devi guadagnare di più. Paga prima te stesso."]
def ease(x): x=max(0.0,min(1.0,x)); return x*x*(3-2*x)
def lerp(a,b,t): return a+(b-a)*t
def eur(v,dec=False): 
    s=f"{v:,.2f}" if dec else f"{int(round(v)):,}"
    s=s.replace(",","X").replace(".",",").replace("X","."); return s+" €"
def wrap(d,t,font,maxw):
    out=[];c=""
    for w in t.split(" "):
        x=(c+" "+w).strip()
        if d.textlength(x,font=font)<=maxw: c=x
        else: out.append(c); c=w
    out.append(c); return out
def ctext(d,y,t,font,fill,maxw=940,lh=1.15):
    for l in wrap(d,t,font,maxw): d.text((W//2,y),l,font=font,fill=fill,anchor="ma"); y+=int(font.size*lh)
    return y
def figure(d,x,y,s=1.0,arm=None):
    d.ellipse([x-38*s,y-200*s,x+38*s,y-124*s],fill=WH)
    d.rounded_rectangle([x-60*s,y-110*s,x+60*s,y+40*s],radius=int(55*s),fill=WH)
    if arm is not None:
        ax=x+60*s; ay=y-70*s; ex=ax+lerp(150,190,arm)*s; ey=ay+lerp(-10,-40,arm)*s
        d.line([ax,ay,ex,ey],fill=WH,width=int(26*s)); d.ellipse([ex-16*s,ey-16*s,ex+16*s,ey+16*s],fill=WH)
def desk(d,x,y):
    d.rectangle([x-40,y,x+520,y+14],fill=WH); d.rectangle([x+480,y+14,x+494,y+150],fill=WH)
    for k in range(0,1080,40): d.line([k,y+170,k+20,y+170],fill=GR,width=3)
def monitor(d,x,y,label,value,col,sub=None):
    d.rounded_rectangle([x,y,x+500,y+300],radius=22,outline=WH,width=8,fill=(18,18,22))
    d.rectangle([x+235,y+300,x+265,y+360],fill=WH)
    d.text((x+250,y+60),label,font=SCRS,fill=GR,anchor="mm"); d.text((x+250,y+150),value,font=SCR,fill=col,anchor="mm")
    if sub: d.text((x+250,y+235),sub,font=SCRS,fill=GR,anchor="mm")
def box(d,x,y,w,h,label,val,col):
    d.rounded_rectangle([x,y,x+w,y+h],radius=20,outline=col,width=6,fill=(18,18,22))
    d.text((x+w//2,y+50),label,font=SCRS,fill=GR,anchor="mm"); d.text((x+w//2,y+125),val,font=MID,fill=col,anchor="mm")
def scene(t):
    for i,(a,b) in enumerate(T):
        nb = T[i+1][0] if i+1<len(T) else b+0.3
        if t<nb: return i,(t-a)/max(0.01,(b-a))
    return 7,0
def frame(t):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    i,p=scene(t); q=ease(p*1.5); arm=0.5+0.5*math.sin(t*6)
    if i==0:
        d.text((W//2,300),"GIORNO",font=K,fill=GR,anchor="mm"); d.text((W//2,390),"1",font=DAYF,fill=WH,anchor="mm")
        monitor(d,470,600,"STIPENDIO",("+"+eur(lerp(0,1400,q))),GREEN,"Marco, 22 anni"); desk(d,330,1170); figure(d,290,1170,arm=arm)
    elif i==1:
        d.text((W//2,300),"GIORNO",font=K,fill=GR,anchor="mm"); d.text((W//2,390),str(int(lerp(1,30,q))),font=DAYF,fill=WH,anchor="mm")
        monitor(d,470,600,"SUL CONTO",eur(lerp(1400,0,q),True),RED if q>0.5 else WH); desk(d,330,1170); figure(d,290,1170,arm=0)
    elif i==2:
        d.text((W//2,300),"OGNI MESE",font=K,fill=GR,anchor="mm")
        mesi=["GEN","FEB","MAR","APR","MAG","GIU","LUG","AGO","SET","OTT","NOV","DIC"]; n=int(lerp(1,12,ease(p*1.2)))
        for k in range(n):
            x=90+(k%4)*230; y=420+(k//4)*190
            d.rounded_rectangle([x,y,x+210,y+160],radius=16,outline=GR,width=3); d.text((x+105,y+45),mesi[k],font=SCRS,fill=GR,anchor="mm"); d.text((x+105,y+108),"0 €",font=MID,fill=RED,anchor="mm")
        figure(d,540,1250)
    elif i==3:
        d.text((W//2,520),"UNA SOLA",font=BIG,fill=WH,anchor="mm"); d.text((W//2,640),"REGOLA",font=BIG,fill=GOLD,anchor="mm"); figure(d,540,1150,s=1.1)
    elif i==4:
        box(d,290,330,500,200,"STIPENDIO","1.400 €",WH)
        a=ease(p*1.4)
        d.line([440,540,lerp(440,250,a),lerp(540,760,a)],fill=GOLD,width=10); d.line([640,540,lerp(640,830,a),lerp(540,760,a)],fill=GR,width=10)
        if a>0.5:
            box(d,60,770,420,200,"CONTO A PARTE","140 €",GOLD); box(d,600,770,420,200,"SPESE","1.260 €",GR)
            d.text((270,1010),"10% · subito",font=SCRS,fill=GOLD,anchor="mm")
        figure(d,540,1330,s=0.9)
    elif i==5:
        m=int(lerp(1,12,q)); v=140*m
        d.text((W//2,300),"MESE",font=K,fill=GR,anchor="mm"); d.text((W//2,390),str(m),font=DAYF,fill=WH,anchor="mm")
        monitor(d,470,600,"CONTO A PARTE",eur(v),GREEN,"140 € al mese"); desk(d,330,1170); figure(d,290,1170,arm=arm)
    elif i==6:
        d.text((W//2,520),"Non devi guadagnare di più.",font=MID,fill=WH,anchor="mm")
        d.text((W//2,660),"Paga prima",font=BIG,fill=GOLD,anchor="mm"); d.text((W//2,770),"te stesso.",font=BIG,fill=GOLD,anchor="mm")
        figure(d,540,1180,s=1.1)
    else:
        d.text((W//2,600),"Paga prima te stesso.",font=MID,fill=GOLD,anchor="mm")
        d.rounded_rectangle([140,760,940,880],radius=60,outline=GOLD,width=4)
        d.text((540,820),"Salva e segui @zeni_thdigital",font=f("Inter-SemiBold.otf",44),fill=WH,anchor="mm")
    if i<7: ctext(d,1420,LINES[i],SUB,WH)
    d.text((W//2,1720),"Esempio didattico, senza interessi. Non è consulenza finanziaria.",font=SM,fill=GR,anchor="mm")
    d.rectangle([0,0,int(W*t/DUR),10],fill=GOLD)
    return im
out=sys.argv[1]
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): p.stdin.write(frame(k/FPS).tobytes())
p.stdin.close(); p.wait()
