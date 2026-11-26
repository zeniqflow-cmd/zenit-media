# Reel "omino" stile Zenith: stessa tredicesima, due destini. Marco spende tutto + 3 rate, Sara la divide in 3 parti. Animazione originale, senza audio.
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
# --- Reel 26/11/2026: stessa tredicesima, due destini (stesso stile del modello reel_costi_fondo_beat.py) ---
# Esempio IPOTETICO: tredicesima netta 1.200 €, divisa in 3 parti da 400 €.
# PAC: 400 € versati a fine anno per 20 anni, rendimento costante 5% annuo, senza costi né tasse.
DUR=28.9
T13=1200; PART=T13//3; RATA=200; NRATE=3; IMPREV=400
R=0.05; N=20
VERS=PART*N
FV=PART*((1+R)**N-1)/R          # 13.226,38
GAIN=FV-VERS                     # 5.226,38
# Ritmo: griglia di "C'est La Vie" non ancora misurata in MARKETING.md -> giri regolari da 1,7 s
BEAT=1.7; GRID=[BEAT/4*k for k in range(0,80)]
def pulse(t):
    past=[g for g in GRID if g<=t]
    return math.exp(-(t-past[-1])*9) if past else 0.0
CUTS=[BEAT*3*k for k in range(1,6)]  # 5.1, 10.2, 15.3, 20.4, 25.5
S1,S2,S3,S4,S5=CUTS
MX,LX,FY=300,780,1080
NAVY=(31,42,68)
def bag(d,x,y,s=1.0,fill=WH):
    d.rounded_rectangle([x-50*s,y-55*s,x+50*s,y+55*s],radius=int(10*s),fill=fill)
    d.arc([x-26*s,y-90*s,x+26*s,y-30*s],180,360,fill=fill,width=int(8*s))
    d.text((x,y+5*s),"%",font=P("Bold",int(52*s)),fill=NAVY,anchor="mm")
def jar(d,x,y,label,amount,prog=1.0,gold=False):
    w,h=300,96
    d.rounded_rectangle([x-w/2,y-h/2,x+w/2,y+h/2],radius=22,outline=GOLD if gold else WH,width=4,fill=(24,33,54))
    if prog>0: d.rounded_rectangle([x-w/2+6,y-h/2+6,x-w/2+6+(w-12)*min(1,prog),y+h/2-6],radius=18,fill=(60,72,98))
    d.text((x-w/2+26,y),label,font=P("Medium",30),fill=G1,anchor="lm")
    d.text((x+w/2-24,y),amount,font=P("Bold",38),fill=GOLD if gold else WH,anchor="rm")
def tire(d,x,y,r=90,t=0):
    d.ellipse([x-r,y-r,x+r,y+r],outline=WH,width=26)
    d.ellipse([x-r*0.38,y-r*0.38,x+r*0.38,y+r*0.38],fill=G1)
    for k in range(6):
        a=t*1.5+k*math.pi/3
        d.line([x+r*0.38*math.cos(a),y+r*0.38*math.sin(a),x+r*0.72*math.cos(a),y+r*0.72*math.sin(a)],fill=G2,width=6)
    # chiodo + aria che esce
    d.line([x+r*0.7,y-r*0.7,x+r*1.05,y-r*1.05],fill=GOLD,width=8)
    for k in range(3):
        ph=(t*2+k/3)%1
        d.arc([x+r*0.9+ph*60-20,y-r*0.9-ph*60-20,x+r*0.9+ph*60+20,y-r*0.9-ph*60+20],200,340,fill=G1,width=4)
def frame(t):
    im=BG.copy(); d=ImageDraw.Draw(im)
    # 1. presentazione: stessa tredicesima
    if t<S1:
        a=back(t/0.6)
        spaced(d,(W/2,300),"DICEMBRE · TREDICESIMA",P("Medium",34),G1,0.2)
        d.text((W/2,410),eur(T13),font=P("Bold",max(10,int(120*min(1,a)))),fill=WH,anchor="mm")
        spaced(d,(W/2,500),"NETTI, A TESTA",P("Medium",30),G1,0.2)
        figure(d,MX,FY,mood="idle",t=t); figure(d,LX,FY,mood="idle",t=t+1)
        spaced(d,(MX,FY+120),"SARA",P("Bold",34),WH,0.2); spaced(d,(LX,FY+120),"MARCO",P("Bold",34),WH,0.2)
        if t>1.7:
            for k,cx in enumerate((MX,LX)):
                for j in range(3):
                    tt=t-1.7-j*0.25-k*0.1
                    if tt>0:
                        yy=lerp(560,770,ease(tt/0.6)); coin(d,cx-60+j*60,int(yy))
        if t>3.4: tag(d,W/2,650,"UNA SOLA DIFFERENZA: COME LA USANO",True)
        return im
    # 2. Black Friday: Marco spende tutto + 3 rate, Sara divide in 3
    if t<S2:
        tt=t-S1
        spaced(d,(W/2,280),"BLACK FRIDAY",P("Medium",34),G1,0.25)
        # Sara: tre parti
        for j,(lab,am) in enumerate([("FONDO",eur(PART)),("PAC",eur(PART)),("PER ME",eur(PART))]):
            p=ease((tt-0.4-j*0.6)/0.6)
            if p>0: jar(d,MX,420+j*125,lab,am,p,gold=(lab=="PAC"))
        figure(d,MX,FY+40,mood="idle",t=t); spaced(d,(MX,FY+160),"SARA",P("Bold",34),WH,0.2)
        # Marco: borse della spesa e rate
        nb=min(4,int(tt/0.425)+1)
        for j in range(nb):
            bx=LX-60+(j%2)*120; by=450+(j//2)*140
            bag(d,bx,by,0.9)
        figure(d,LX,FY+40,mood="happy",t=t)
        spaced(d,(LX,FY+160),"MARCO",P("Bold",34),WH,0.2)
        if tt>2.55: tag(d,LX,720,f"+{NRATE} RATE DA {RATA} €",True)
        return im
    # 3. gennaio: l'imprevisto
    if t<S3:
        tt=t-S2
        spaced(d,(W/2,280),"GENNAIO · IMPREVISTO",P("Medium",34),G1,0.2)
        tire(d,W/2-130,450,85,t)
        d.text((W/2+110,450),eur(IMPREV),font=P("Bold",96),fill=GOLD,anchor="mm")
        if tt>1.0:
            tag(d,MX,620,"PAGA COL FONDO")
            if tt>1.85: tag(d,MX,705,"PAC INTATTO",True)
        if tt>1.4:
            tag(d,LX,620,f"RATA {RATA} €")
            if tt>2.25: tag(d,LX,705,f"NUOVO DEBITO {IMPREV} €",True)
        figure(d,MX,FY+40,mood="happy" if tt>1.85 else "idle",t=t); spaced(d,(MX,FY+160),"SARA",P("Bold",34),WH,0.2)
        if tt>1.85: sparkle(d,MX,FY-80,t,0.8)
        figure(d,LX,FY+40,mood="sad",t=t); spaced(d,(LX,FY+160),"MARCO",P("Bold",34),WH,0.2)
        if tt>1.4: cloud(d,LX,FY-215,t)
        return im
    # 4. ogni dicembre, per 20 anni
    if t<S4:
        tt=t-S3; p=ease((tt-0.4)/3.0)
        spaced(d,(W/2,280),f"OGNI DICEMBRE · PER {N} ANNI",P("Medium",34),G1,0.15)
        monitor(d,MX,590,440,230,"SARA · PAC",eur(lerp(0,FV,p)),64)
        monitor(d,LX,590,440,230,"MARCO · PAC",eur(0),64)
        yr=min(N,int(p*N+0.0001))
        spaced(d,(W/2,370),f"ANNO {max(1,yr)} DI {N}",P("Medium",30),G1,0.2)
        figure(d,MX,FY+40,mood="happy",t=t); sparkle(d,MX,FY-110,t)
        figure(d,LX,FY+40,mood="sad",t=t); cloud(d,LX,FY-260,t)
        return im
    # 5. il concetto: paga prima te stesso + interesse composto
    if t<S5:
        tt=t-S4; p=ease(tt/1.2); q=ease((tt-1.0)/1.2)
        spaced(d,(W/2,280),"PAGA PRIMA TE STESSO",P("Medium",34),G1,0.2)
        x0,x1=150,930
        wv=(x1-x0)*VERS/FV
        d.text((x0,400),"VERSATI",font=P("Medium",30),fill=G1,anchor="lm")
        d.text((x1,400),eur(VERS),font=P("Bold",40),fill=WH,anchor="rm")
        d.rounded_rectangle([x0,430,x0+max(40,wv*p),490],radius=30,fill=WH)
        d.text((x0,560),"VALORE",font=P("Medium",30),fill=G1,anchor="lm")
        d.text((x1,560),"circa "+eur(FV),font=P("Bold",40),fill=WH,anchor="rm")
        d.rounded_rectangle([x0,590,x0+max(40,(x1-x0)*q),650],radius=30,fill=GOLD)
        if tt>2.2:
            pp=back((tt-2.2)/0.5)
            d.text((W/2,760),"+"+eur(GAIN),font=P("Bold",max(10,int(96*min(1,pp)))),fill=GOLD,anchor="mm")
            spaced(d,(W/2,850),"DI INTERESSE COMPOSTO",P("Medium",32),G1,0.15)
        figure(d,W/2,FY+170,mood="happy" if tt>2.2 else "idle",t=t,s=0.8)
        return im
    # 6. chiusura
    tt=t-S5; p=back(tt/0.5); sz=int(76*max(0.05,min(1.05,p)))
    d.text((W/2,400),"Stessa tredicesima.",font=P("Bold",sz),fill=WH,anchor="mm")
    d.text((W/2,500),"Due destini.",font=P("Bold",sz),fill=GOLD,anchor="mm")
    d.rounded_rectangle([150,650,930,770],radius=60,fill=GOLD)
    d.text((W/2,710),"Commenta ZEN per il regalo",font=P("Bold",44),fill=NAVY,anchor="mm")
    d.rounded_rectangle([170,810,910,920],radius=55,outline=GOLD,width=5)
    d.text((W/2,865),"Salva e segui @zeni_thdigital",font=P("Medium",40),fill=WH,anchor="mm")
    figure(d,W/2,FY+180,s=0.9,mood="happy",t=t)
    return im
SUBS=[(0.0,S1,"Marco e Sara ricevono la stessa tredicesima: 1.200 €."),
      (S1,S2,"Black Friday. Marco spende tutto e apre 3 rate. Sara fa 3 parti da 400 €."),
      (S2,S3,"Gomma bucata: 400 €. Marco fa un nuovo debito, Sara usa il fondo."),
      (S3,S4,"Se Sara mette 400 € nel PAC ogni dicembre, dopo 20 anni..."),
      (S4,S5,"8.000 € versati, circa 13.200 € di valore. Il resto è interesse composto."),]
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
                d.text((W/2,y),l,font=f,fill=NAVY,anchor="mm"); y+=84
def post(im,t):
    glow=im.filter(ImageFilter.GaussianBlur(14))
    out=ImageChops.add(im,ImageChops.multiply(glow,Image.new("RGB",(W,H),(90,80,60))))
    d=ImageDraw.Draw(out)
    subs(d,t)
    if S3<=t<S5: note="Ipotesi: 400 € a fine anno, 5% annuo costante, senza costi né tasse."
    else: note="Esempio ipotetico con cifre inventate a scopo didattico."
    d.text((W/2,1630),note,font=P("Regular",26),fill=(150,160,180),anchor="mm")
    d.text((W/2,1665),"I rendimenti non sono garantiti. Non è consulenza finanziaria.",font=P("Regular",26),fill=(150,160,180),anchor="mm")
    if pulse(t)>0.6: out=Image.blend(out,Image.new("RGB",(W,H),(201,164,76)),0.05*pulse(t))
    for c in CUTS:
        if 0<=t-c<0.12: out=Image.blend(out,Image.new("RGB",(W,H),(201,164,76)),0.25*(1-(t-c)/0.12))
    return out
if __name__=="__main__":
    print(f"versati {VERS}, valore {FV:.2f}, interesse {GAIN:.2f}",file=sys.stderr)
    out=sys.argv[1]
    if len(sys.argv)>2:  # anteprima fotogrammi: python3 script.py out_dir t1 t2 ...
        for s in sys.argv[2:]:
            t=float(s); post(frame(t),t).save(f"{out}/f_{s}.png")
        sys.exit()
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-vf","setsar=1","-c:a","aac","-b:a","128k","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for k in range(int(DUR*FPS)):
        t=k/FPS; p.stdin.write(post(frame(t),t).tobytes())
    p.stdin.close(); p.wait()
