# Reel "omino" stile Zenith: Sara resta investita, Paolo esce nel panico e perde i 10 giorni migliori. Animazione originale, senza audio.
import sys,subprocess,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
FP="/usr/share/fonts/truetype/google-fonts/"
_C={}
def P(w,s):
    k=(w,s)
    if k not in _C: _C[k]=ImageFont.truetype("/usr/share/fonts/opentype/inter/"+{"Bold":"InterDisplay-Bold.otf","Medium":"Inter-Medium.otf","Regular":"Inter-Regular.otf"}[w],s)
    return _C[k]
W,H,FPS=1080,1920,30; DUR=30.0
WH=(245,241,232); G1=(143,169,152); G2=(70,84,110); G3=(38,48,70); GOLD=(201,164,76)
def ease(x): x=max(0.0,min(1.0,x)); return x*x*(3-2*x)
def back(x): x=max(0.0,min(1.0,x)); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def lerp(a,b,t): return a+(b-a)*t
def eur(v): return f"{int(round(v)):,}".replace(",",".")+" €"
def spaced(d,xy,t,font,fill,sp=0.12,anchor="mm"):
    ws=[d.textlength(c,font=font) for c in t]; tw=sum(ws)+sp*font.size*(len(t)-1)
    x,y=xy; x0=x-tw/2 if anchor[0]=="m" else x
    for c,w in zip(t,ws): d.text((x0,y),c,font=font,fill=fill,anchor="l"+anchor[1]); x0+=w+sp*font.size
# sfondo: griglia di punti + vignettatura
BG=Image.new("RGB",(W,H),(31,42,68)); bd=ImageDraw.Draw(BG)
for y in range(20,H,54):
    for x in range(20,W,54): bd.ellipse([x-2,y-2,x+2,y+2],fill=(48,60,88))
vig=Image.new("L",(W,H),0); vd=ImageDraw.Draw(vig); vd.ellipse([-300,200,W+300,H-200],fill=255); vig=vig.filter(ImageFilter.GaussianBlur(260))
BG=Image.composite(BG,Image.new("RGB",(W,H),(18,25,42)),vig)
def figure(d,x,y,s=1.0,mood="idle",t=0,arm=None):
    bob=0; head_dx=0; head_dy=0; slump=0
    if mood=="idle": bob=-14*pulse(t)
    if mood=="happy": bob=-46*pulse(t)
    if mood=="sad": head_dx=18; head_dy=34; slump=24
    y=y+bob
    # ombra ellittica tratteggiata
    for k in range(0,360,20): 
        a1=math.radians(k); a2=math.radians(k+10)
        d.line([x+110*s*math.cos(a1),y+48*s+20*s*math.sin(a1),x+110*s*math.cos(a2),y+48*s+20*s*math.sin(a2)],fill=G1,width=3)
    # corpo
    top=y-120*s+slump
    d.rounded_rectangle([x-62*s,top,x+62*s,y+40*s],radius=int(48*s),fill=WH)
    # braccia
    if mood=="happy":
        for sx in (-1,1):
            d.line([x+sx*50*s,top+30*s,x+sx*110*s,top-90*s],fill=WH,width=int(28*s)); d.ellipse([x+sx*110*s-16*s,top-106*s,x+sx*110*s+16*s,top-74*s],fill=WH)
    elif mood=="sad":
        for sx in (-1,1):
            d.line([x+sx*58*s,top+30*s,x+sx*72*s,top+120*s],fill=WH,width=int(26*s))
    elif arm is not None:
        ax=x+55*s; ay=top+35*s; ex=ax+150*s; ey=ay+arm*s
        d.line([ax,ay,ex,ey],fill=WH,width=int(28*s)); d.ellipse([ex-16*s,ey-16*s,ex+16*s,ey+16*s],fill=WH)
    # testa
    hx=x+head_dx*s; hy=top-58*s+head_dy*s
    d.ellipse([hx-48*s,hy-48*s,hx+48*s,hy+48*s],fill=WH)
    return top
def cloud(d,x,y,t):
    for dx,r in [(-50,38),(0,52),(55,40)]: d.ellipse([x+dx-r,y-r,x+dx+r,y+r],fill=G2)
    for k in range(6):
        ph=(t*1.6+k/6)%1; xx=x-70+k*28; yy=y+40+ph*140
        d.line([xx,yy,xx-6,yy+26],fill=G1,width=5)
def sparkle(d,x,y,t,s=1):
    for k in range(5):
        a=t*2+k*1.256; r=120+20*math.sin(t*5+k)
        px=x+r*math.cos(a); py=y-40+r*0.6*math.sin(a)
        L=14*s*(0.6+0.4*math.sin(t*9+k))
        d.line([px-L,py,px+L,py],fill=WH,width=4); d.line([px,py-L,px,py+L],fill=WH,width=4)
def monitor(d,x,y,w,h,title,value,big):
    d.rounded_rectangle([x-w/2,y-h/2,x+w/2,y+h/2],radius=18,outline=WH,width=6,fill=(24,33,54))
    d.rectangle([x-12,y+h/2,x+12,y+h/2+40],fill=G1); d.rectangle([x-50,y+h/2+40,x+50,y+h/2+48],fill=G1)
    spaced(d,(x,y-h/2+42),title,P("Medium",24),G1,0.18)
    d.text((x,y+18),value,font=P("Bold",big),fill=WH,anchor="mm")
def bank(d,x,y,s=1.0):
    d.polygon([(x-110*s,y-150*s),(x,y-215*s),(x+110*s,y-150*s)],fill=G1)
    for k in range(4): xx=x-80*s+k*53*s; d.rectangle([xx-12*s,y-140*s,xx+12*s,y-30*s],fill=G1)
    d.rectangle([x-120*s,y-30*s,x+120*s,y-10*s],fill=G1)
    spaced(d,(x,y+25*s),"BANCA",P("Bold",int(30*s)),G1,0.2)
def laptop(d,x,y):
    d.rounded_rectangle([x-90,y-120,x+90,y-10],radius=8,outline=WH,width=5); d.rectangle([x-115,y-10,x+115,y+5],fill=WH)
    spaced(d,(x,y-65),"ETF",P("Bold",40),WH,0.15)
def tag(d,x,y,t,strong=False):
    f=P("Bold",34); w=d.textlength(t,font=f)+60
    d.rounded_rectangle([x-w/2,y-34,x+w/2,y+34],radius=34,fill=GOLD if strong else None,outline=GOLD if strong else WH,width=4)
    d.text((x,y),t,font=f,fill=(31,42,68) if strong else WH,anchor="mm")
def coin(d,x,y,r=26):
    d.ellipse([x-r,y-r,x+r,y+r],outline=WH,width=5); d.text((x,y),"€",font=P("Bold",int(r*1.2)),fill=WH,anchor="mm")
# --- Reel 24/11/2026: fuori dal mercato nei 10 giorni migliori (stesso stile del modello reel_costi_fondo_beat.py) ---
DUR=28.9
def usd(v): return f"{int(round(v)):,}".replace(",",".")+" $"
# Dati reali (Motley Fool, ott. 2026, ETF SPY con dividendi reinvestiti, 12/10/2006-12/10/2026)
START=10000; FULL=82300; MISS10=35700
CAGR_F=(FULL/START)**(1/20)-1; CAGR_M=(MISS10/START)**(1/20)-1; DIFF=FULL-MISS10; LOSS=1-MISS10/FULL
BEAT=1.7; GRID=[BEAT/4*k for k in range(0,80)]
def pulse(t):
    past=[g for g in GRID if g<=t]
    return math.exp(-(t-past[-1])*9) if past else 0.0
CUTS=[BEAT*3*k for k in range(1,6)]  # 5.1, 10.2, 15.3, 20.4, 25.5
S1,S2,S3,S4,S5=CUTS
MX,LX,FY=300,780,1080
def chart(d,x0,y0,w,h,prog):
    # andamento ILLUSTRATIVO (non dati reali): sale, crolla, riparte
    pts=[(0,0.55),(0.15,0.42),(0.3,0.35),(0.42,0.85),(0.5,0.92),(0.58,0.6),(0.7,0.45),(0.85,0.3),(1,0.12)]
    n=int(60*prog); P_=[]
    for k in range(n+1):
        u=k/60
        for (a,ya),(b,yb) in zip(pts,pts[1:]):
            if a<=u<=b: v=lerp(ya,yb,ease((u-a)/(b-a))); break
        P_.append((x0+u*w,y0+v*h))
    d.line([(x0,y0+h),(x0+w,y0+h)],fill=G2,width=4)
    if len(P_)>1: d.line(P_,fill=GOLD,width=8,joint="curve")
    if P_: d.ellipse([P_[-1][0]-12,P_[-1][1]-12,P_[-1][0]+12,P_[-1][1]+12],fill=WH)
    return P_
def frame(t):
    im=BG.copy(); d=ImageDraw.Draw(im)
    # 1. presentazione
    if t<S1:
        a=back(t/0.6)
        spaced(d,(W/2,300),"STESSO ETF S&P 500 · 2006",P("Medium",34),G1,0.2)
        d.text((W/2,400),"10.000 $",font=P("Bold",max(10,int(110*min(1,a)))),fill=WH,anchor="mm")
        figure(d,MX,FY,mood="idle",t=t); figure(d,LX,FY,mood="idle",t=t+1)
        spaced(d,(MX,FY+120),"SARA",P("Bold",34),WH,0.2); spaced(d,(LX,FY+120),"PAOLO",P("Bold",34),WH,0.2)
        if t>1.7:
            p=back((t-1.7)/0.5); laptop(d,MX,int(FY-255+(1-min(1,p))*120)); laptop(d,LX,int(FY-255+(1-min(1,p))*120))
        if t>3.4: tag(d,W/2,FY-480,"UNA SOLA DIFFERENZA",True)
        return im
    # 2. il crollo: Paolo esce
    if t<S2:
        tt=t-S1; prog=min(1,0.45+tt/5.1*0.2)
        spaced(d,(W/2,280),"2008 · LA BORSA CROLLA",P("Medium",34),G1,0.2)
        chart(d,140,380,800,300,prog)
        figure(d,MX,FY+40,mood="idle",t=t); spaced(d,(MX,FY+160),"SARA",P("Bold",34),WH,0.2)
        tag(d,MX,FY-330,"RESTO")
        px=LX+ease((tt-1.7)/2.5)*420 if tt>1.7 else LX
        figure(d,px,FY+40,mood="sad",t=t); cloud(d,px,FY-260,t)
        if px<W-60: spaced(d,(px,FY+160),"PAOLO",P("Bold",34),WH,0.2)
        if tt<3.4: tag(d,LX,FY-330,"VENDO TUTTO!",True)
        return im
    # 3. i giorni migliori arrivano mentre Paolo è fuori
    if t<S3:
        tt=t-S2
        spaced(d,(W/2,280),"I 10 GIORNI MIGLIORI IN 20 ANNI",P("Medium",34),G1,0.12)
        d.text((W/2,400),"+14,5%",font=P("Bold",130),fill=GOLD,anchor="mm")
        spaced(d,(W/2,500),"IN UN SOLO GIORNO · 13/10/2008",P("Medium",30),G1,0.12)
        lit=min(10,int(tt/0.425)+1)
        for k in range(10):
            r,c=divmod(k,5); x=200+c*170; y=640+r*150
            on=k<lit
            d.rounded_rectangle([x-65,y-55,x+65,y+55],radius=16,fill=GOLD if on else None,outline=GOLD if on else G2,width=4)
            d.text((x,y),f"{k+1}",font=P("Bold",48),fill=(31,42,68) if on else G2,anchor="mm")
        figure(d,MX,FY+140,mood="happy",t=t,s=0.8); sparkle(d,MX,FY+40,t)
        figure(d,LX+120,FY+140,mood="sad",t=t,s=0.8)
        tag(d,LX+60,FY-90,"PAOLO È FUORI")
        return im
    # 4. il verdetto
    if t<S4:
        tt=t-S3; p=ease(tt/2.2)
        spaced(d,(W/2,280),"OTTOBRE 2026 · 20 ANNI DOPO",P("Medium",34),G1,0.15)
        monitor(d,MX,620,420,230,"SARA · SEMPRE DENTRO",usd(lerp(START,FULL,p)),62)
        monitor(d,LX,620,420,230,"PAOLO · NEL PANICO",usd(lerp(START,MISS10,p)),62)
        figure(d,MX,FY+40,mood="happy",t=t); sparkle(d,MX,FY-110,t)
        figure(d,LX,FY+40,mood="sad",t=t); cloud(d,LX,FY-280,t)
        return im
    # 5. il concetto
    if t<S5:
        tt=t-S4; p=ease(tt/1.5)
        d.text((W/2,330),"−"+usd(DIFF*p),font=P("Bold",120),fill=GOLD,anchor="mm")
        spaced(d,(W/2,450),"PER 10 GIORNI SU CIRCA 5.000",P("Medium",32),G1,0.12)
        for k in range(10):
            x=150+k*87; y=640; on=k<7
            d.ellipse([x-30,y-30,x+30,y+30],fill=GOLD if on else None,outline=GOLD if on else G2,width=5)
        d.text((W/2,770),"7 su 10 sono arrivati",font=P("Bold",60),fill=WH,anchor="mm")
        d.text((W/2,850),"entro 2 settimane",font=P("Bold",60),fill=WH,anchor="mm")
        d.text((W/2,930),"dai giorni peggiori.",font=P("Bold",60),fill=WH,anchor="mm")
        figure(d,W/2,FY+170,mood="idle",t=t,s=0.8)
        return im
    # 6. chiusura
    tt=t-S5; p=back(tt/0.5); sz=int(78*max(0.05,min(1.05,p)))
    d.text((W/2,420),"Il tempo nel mercato",font=P("Bold",sz),fill=WH,anchor="mm")
    d.text((W/2,520),"batte il market timing.",font=P("Bold",sz),fill=WH,anchor="mm")
    d.rounded_rectangle([150,650,930,770],radius=60,fill=GOLD)
    d.text((W/2,710),"Commenta ZEN per il regalo",font=P("Bold",44),fill=(31,42,68),anchor="mm")
    d.rounded_rectangle([170,810,910,920],radius=55,outline=GOLD,width=5)
    d.text((W/2,865),"Salva e segui @zeni_thdigital",font=P("Medium",40),fill=WH,anchor="mm")
    figure(d,W/2,FY+180,s=0.9,mood="happy",t=t)
    return im
SUBS=[(0.0,S1,"Sara e Paolo investono 10.000 $ a testa in un ETF sull'S&P 500."),
      (S1,S2,"Nel 2008 la borsa crolla. Paolo vende per paura. Sara resta."),
      (S2,S3,"Ma i giorni migliori arrivano proprio lì, in mezzo al panico."),
      (S3,S4,"Paolo perde solo i 10 giorni migliori. Sara resta investita."),
      (S4,S5,"Quasi 47 mila $ in meno: più della metà del risultato."),]
def subs(d,t):
    for a,b,txt in SUBS:
        if a<=t<b:
            f=P("Bold",50); words=txt.split(); lines=[];c=""
            for w in words:
                x=(c+" "+w).strip()
                if d.textlength(x,font=f)<=900: c=x
                else: lines.append(c); c=w
            lines.append(c)
            y=1400
            for l in lines:
                tw=d.textlength(l,font=f); d.rounded_rectangle([W/2-tw/2-24,y-38,W/2+tw/2+24,y+38],radius=18,fill=(245,241,232))
                d.text((W/2,y),l,font=f,fill=(31,42,68),anchor="mm"); y+=84
def post(im,t):
    glow=im.filter(ImageFilter.GaussianBlur(14))
    out=ImageChops.add(im,ImageChops.multiply(glow,Image.new("RGB",(W,H),(90,80,60))))
    d=ImageDraw.Draw(out)
    subs(d,t)
    note="Grafico illustrativo." if S1<=t<S2 else "Dati storici S&P 500 (SPY, dividendi reinvestiti) 2006-2026."
    d.text((W/2,1630),note+" Fonte: Motley Fool.",font=P("Regular",26),fill=(150,160,180),anchor="mm")
    d.text((W/2,1665),"Scenario ipotetico. Non è consulenza finanziaria.",font=P("Regular",26),fill=(150,160,180),anchor="mm")
    if pulse(t)>0.6: out=Image.blend(out,Image.new("RGB",(W,H),(201,164,76)),0.05*pulse(t))
    for c in CUTS:
        if 0<=t-c<0.12: out=Image.blend(out,Image.new("RGB",(W,H),(201,164,76)),0.25*(1-(t-c)/0.12))
    return out
if __name__=="__main__":
    print(f"CAGR sempre dentro {CAGR_F:.2%}, senza 10 giorni {CAGR_M:.2%}, differenza {DIFF}, perdita {LOSS:.1%}",file=sys.stderr)
    out=sys.argv[1]
    if len(sys.argv)>2:  # anteprima fotogrammi: python3 script.py out_dir t1 t2 ...
        for s in sys.argv[2:]:
            t=float(s); post(frame(t),t).save(f"{out}/f_{s}.png")
        sys.exit()
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-vf","setsar=1","-c:a","aac","-b:a","128k","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for k in range(int(DUR*FPS)):
        t=k/FPS; p.stdin.write(post(frame(t),t).tobytes())
    p.stdin.close(); p.wait()
