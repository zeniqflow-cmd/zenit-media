# Reel "omino" stile minimal luminoso: due amici, stessi soldi, costi diversi. Animazione originale, senza audio.
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
def fv(r,years):
    i=(1+r)**(1/12)-1; v=0
    for k in range(int(round(years*12))): v=v*(1+i)+200
    return v
CURVE={k:(fv(0.038,k),fv(0.058,k)) for k in range(31)}
def val(y,idx):
    a=int(y); b=min(30,a+1); f=y-a
    return lerp(CURVE[a][idx],CURVE[b][idx],f)
def figure(d,x,y,s=1.0,mood="idle",t=0,arm=None):
    bob=0; head_dx=0; head_dy=0; slump=0
    if mood=="idle": bob=4*math.sin(t*3)
    if mood=="happy": bob=-abs(40*math.sin(t*7))
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
MX,LX,FY=300,780,1080
def frame(t):
    im=BG.copy(); d=ImageDraw.Draw(im)
    # 1. presentazione
    if t<10.5:
        a=back(t/0.6)
        spaced(d,(W/2,300),"STESSI SOLDI",P("Medium",34),G1,0.25)
        d.text((W/2,390),"200 € / MESE",font=P("Bold",int(96*min(1,a))) if a>0.05 else P("Bold",10),fill=WH,anchor="mm")
        figure(d,MX,FY,mood="idle",t=t); figure(d,LX,FY,mood="idle",t=t+1)
        spaced(d,(MX,FY+120),"MARCO",P("Bold",34),WH,0.2); spaced(d,(LX,FY+120),"LUCA",P("Bold",34),WH,0.2)
        if t>3.5:
            p=back((t-3.5)/0.5); bank(d,MX,FY-300,s=max(0.01,p)); 
            if t>4.3: tag(d,MX,FY-560,"COSTI 2,2%")
        if t>7.0:
            p=back((t-7.0)/0.5); laptop(d,LX,int(FY-255+(1-min(1,p))*120))
            if t>7.8: tag(d,LX,FY-560,"COSTI 0,2%",True)
        if t>3.5: 
            for k in range(3):
                ph=((t*0.9)+k/3)%1; coin(d,MX+150,lerp(FY-40,FY-420,ph),18)
        return im
    # 2. trent'anni che scorrono
    if t<16:
        p=ease((t-10.5)/5.2); y=30*p
        spaced(d,(W/2,280),"ANNI",P("Medium",34),G1,0.3)
        d.text((W/2,380),f"{int(y)}",font=P("Bold",150),fill=WH,anchor="mm")
        vm,vl=val(y,0),val(y,1)
        monitor(d,MX,760,400,230,"MARCO · BANCA",eur(vm),62); monitor(d,LX,760,400,230,"LUCA · ETF",eur(vl),62)
        # barre di crescita
        figure(d,MX,FY+80,mood="idle",t=t,arm=None); figure(d,LX,FY+80,mood="idle",t=t+1)
        return im
    # 3. il verdetto: emozioni
    if t<19.5:
        tt=t-16
        spaced(d,(W/2,280),"DOPO 30 ANNI",P("Medium",34),G1,0.3)
        monitor(d,MX,620,400,230,"MARCO",eur(132446),62); monitor(d,LX,620,400,230,"LUCA",eur(188012),62)
        figure(d,MX,FY,mood="sad",t=t); cloud(d,MX,FY-320,t)
        figure(d,LX,FY,mood="happy",t=t); sparkle(d,LX,FY-150,t)
        spaced(d,(W/2,1240),"HANNO VERSATO ENTRAMBI 72.000 €",P("Bold",34),WH,0.06)
        return im
    # 4. dove sono finiti i soldi
    if t<23.5:
        tt=t-19.5
        bank(d,LX-30,820,s=1.6)
        figure(d,MX-60,FY+40,mood="sad",t=t); cloud(d,MX-60,FY-280,t)
        for k in range(7):
            ph=((tt*0.8)+k/7)%1; x=lerp(MX,LX-30,ph); y=lerp(FY-200,700,ph)-180*math.sin(ph*math.pi)
            coin(d,x,y,24)
        n=55566*ease(tt/2.5)
        d.text((W/2,330),"−"+eur(n),font=P("Bold",120),fill=GOLD,anchor="mm")
        spaced(d,(W/2,450),"TRA COMMISSIONI E INTERESSI PERSI",P("Medium",30),G1,0.12)
        return im
    # 5. il concetto
    if t<27.5:
        tt=t-23.5; p=ease(tt/1.5)
        d.text((W/2,360),"Il 2% sembra poco.",font=P("Bold",64),fill=WH,anchor="mm")
        cx,cy,r=W/2,820,260
        d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=G1,width=8)
        d.pieslice([cx-r,cy-r,cx+r,cy+r],-90,-90+360*0.296*p,fill=GOLD)
        d.text((W/2,1170),"Su 30 anni ti costa",font=P("Medium",48),fill=G1,anchor="mm")
        d.text((W/2,1260),"quasi 1/3 dei tuoi soldi.",font=P("Bold",64),fill=WH,anchor="mm")
        return im
    # 6. chiusura
    tt=t-27.5; p=back(tt/0.5)
    d.text((W/2,560),"Controlla il TER",font=P("Bold",int(84*max(0.05,min(1.05,p)))),fill=WH,anchor="mm")
    d.text((W/2,670),"del tuo fondo.",font=P("Bold",int(84*max(0.05,min(1.05,p)))),fill=WH,anchor="mm")
    d.rounded_rectangle([170,830,910,950],radius=60,outline=GOLD,width=5)
    d.text((W/2,890),"Salva e segui @zeni_thdigital",font=P("Medium",40),fill=WH,anchor="mm")
    figure(d,W/2,FY+120,mood="happy",t=t,s=0.9) if False else figure(d,W/2,FY+120,s=0.9,mood="happy",t=t)
    return im
SUBS=[(0.0,3.5,"Due amici. Stessi soldi. Stesso mercato."),(3.5,7.0,"Marco investe in banca: costi del 2,2% l'anno."),(7.0,10.5,"Luca compra un ETF: costi dello 0,2%."),(10.5,16.0,"200 € al mese, per 30 anni."),(16.0,19.5,"Luca ha 188 mila €. Marco solo 132 mila."),(19.5,23.5,"55 mila € persi tra commissioni e interessi mancati."),]
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
    d.text((W/2,1590),"Esempio ipotetico: rendimento lordo 6% annuo costante.",font=P("Regular",26),fill=(150,160,180),anchor="mm")
    d.text((W/2,1625),"Non è consulenza finanziaria.",font=P("Regular",26),fill=(150,160,180),anchor="mm")
    # flash ai cambi scena
    for c in (10.5,16,19.5,23.5,27.5):
        if 0<=t-c<0.12: out=Image.blend(out,Image.new("RGB",(W,H),(201,164,76)),0.25*(1-(t-c)/0.12))
    return out
out=sys.argv[1]
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-vf","setsar=1","-c:a","aac","-b:a","128k","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-movflags","+faststart",out],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)):
    t=k/FPS; p.stdin.write(post(frame(t),t).tobytes())
p.stdin.close(); p.wait()
