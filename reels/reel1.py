import sys,subprocess,math
sys.path.insert(0,'/home/claude/car')
from lib import f,CREAM,NAVY,GOLD,SAGE,RED,LINE
from PIL import Image,ImageDraw
W,H=1080,1920; FPS=30; DUR=28
Z=Image.open('zen440.png').convert('RGBA')
TIT=f("InterDisplay-Bold.otf",76); KICK=f("Inter-SemiBold.otf",32); BUB=f("Inter-SemiBold.otf",40)
BIG=f("InterDisplay-Bold.otf",130); MID=f("InterDisplay-Bold.otf",56); LAB=f("Inter-SemiBold.otf",34); SM=f("Inter-Regular.otf",24); VAL=f("InterDisplay-Bold.otf",44)
def wrap(d,t,font,maxw):
    out=[];c=""
    for w in t.split(" "):
        x=(c+" "+w).strip()
        if d.textlength(x.replace("\u00a0"," "),font=font)<=maxw: c=x
        else: out.append(c); c=w
    out.append(c); return [l.replace("\u00a0"," ") for l in out]
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def seg(t,a,b): return ease((t-a)/(b-a))
def txt(d,x,y,t,font,fill,maxw,lh=1.15,anchor=None):
    for l in wrap(d,t,font,maxw):
        d.text((x,y),l,font=font,fill=fill); y+=int(font.size*lh)
    return y
def eur(v): return f"{int(round(v)):,}".replace(",",".")+" €"
def eurk(v): return f"{int(round(v/1000.0))*1000:,}".replace(",",".")+" €"
VALS=[48000,118196,262481]; NAMES=["Fermi (0%)","4% annuo","7% annuo"]; COLS=[(140,145,155),SAGE,GOLD]
def frame(t):
    im=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,16],fill=GOLD)
    d.text((80,250),"ZENONE SPIEGA",font=KICK,fill=SAGE)
    # titles per scene with fade (simple switch)
    if t<9: title="100\u00a0€ al mese. Quanto diventano in 40 anni?"
    elif t<19: title="Stessi soldi versati, tre risultati"
    elif t<24: title="Da dove arriva la differenza?"
    else: title="Il tempo vale più della cifra."
    txt(d,80,300,title,TIT,NAVY,920)
    # scene 2: counter
    if 4<=t<9:
        a=seg(t,4,6.5); n=int(480*a); v=48000*a
        d.text((W//2,700),f"{n} versamenti",font=MID,fill=NAVY,anchor="mm")
        d.text((W//2,860),eur(v),font=BIG,fill=GOLD,anchor="mm")
        d.text((W//2,980),"messi da parte in 40 anni",font=LAB,fill=NAVY,anchor="mm")
    # scene 3/4: bars
    if 9<=t<24:
        base=1100; maxh=500; bw=200; xs=[150,440,730]
        starts=[9,11.5,14.5]
        for i in range(3):
            g=seg(t,starts[i],starts[i]+2.8)
            h=maxh*VALS[i]/VALS[2]*g
            x=xs[i]
            fade = 1.0
            if t>=19 and i<2: fade=max(0.25,1-seg(t,19,20))
            col=tuple(int(c*fade+245*(1-fade)) if True else c for c in COLS[i])
            if t>=19 and i==2:
                # exploded bar: versati (bottom) and interessi (top) separate
                e=seg(t,19,21)
                hv=maxh*48000/VALS[2]; hi=maxh-hv; gap=60*e; dx=-40*e
                d.rounded_rectangle([x,base-hv,x+bw,base],radius=14,fill=NAVY)
                d.rounded_rectangle([x+dx,base-hv-gap-hi,x+dx+bw,base-hv-gap],radius=14,fill=GOLD)
                if e>0.5:
                    al=seg(t,20,21.5)
                    c1=tuple(int(NAVY[k]*al+245*(1-al)) for k in range(3))
                    c2=tuple(int((140,105,30)[k]*al+245*(1-al)) for k in range(3))
                    d.text((x-20,base-hv/2),"Versati",font=LAB,fill=c1,anchor="rm")
                    d.text((x-20,base-hv/2+40),"48.000 €",font=LAB,fill=c1,anchor="rm")
                    d.text((x+dx-20,base-hv-gap-hi/2),"Interessi",font=LAB,fill=c2,anchor="rm")
                    d.text((x+dx-20,base-hv-gap-hi/2+40),"≈ 214.000 €",font=LAB,fill=c2,anchor="rm")
            else:
                if h>2: d.rounded_rectangle([x,base-h,x+bw,base],radius=14,fill=col)
                if g>0:
                    d.text((x+bw/2,base-h-35),"≈ "+eurk(VALS[i]*g) if i else eur(VALS[i]*g),font=VAL if g<1 else VAL,fill=tuple(int(NAVY[k]*fade+245*(1-fade)) for k in range(3)),anchor="mm")
                    d.text((x+bw/2,base+40),NAMES[i],font=LAB,fill=tuple(int(NAVY[k]*fade+245*(1-fade)) for k in range(3)),anchor="mm")
    # scene 5: CTA
    if t>=24:
        a=seg(t,24,25)
        d.text((W//2,640),"Stessi 100\u00a0€ al mese.",font=MID,fill=NAVY,anchor="mm")
        d.text((W//2,720),"Chi inizia prima, finisce più avanti.",font=MID,fill=NAVY,anchor="mm")
        y=830
        for lab in ["Salva questo video","Segui @zeni_thdigital"]:
            d.rounded_rectangle([140,y,W-140,y+110],radius=55,fill=GOLD if lab.startswith("Segui") else None,outline=GOLD,width=4)
            d.text((W//2,y+55),lab,font=MID if False else f("Inter-SemiBold.otf",44),fill=NAVY,anchor="mm"); y+=140
    # Zenone entrance
    zx=int(-460+500*seg(t,0,1.2)); zy=1180
    bob=int(6*math.sin(t*2.2))
    im.paste(Z,(zx,zy+bob),Z)
    # bubble
    if t<4: btxt="Ciao, sono Zenone. Facciamo due conti."
    elif t<9: btxt="Dai 22 ai 62 anni, sempre 100\u00a0€ al mese."
    elif t<19: btxt="Cambia solo il rendimento, non quanto versi."
    elif t<24: btxt="Oltre l'80% del totale viene dagli interessi: lavora il tempo."
    else: btxt="Salva il video e inizia presto."
    ba=seg(t,1.0,1.6)
    if ba>0:
        bx,by=330,1230
        lines=wrap(d,btxt,BUB,600); bh=len(lines)*52+50
        d.rounded_rectangle([bx,by,bx+680,by+bh],radius=30,fill=NAVY)
        d.polygon([(bx,by+bh-50),(bx-30,by+bh-10),(bx+40,by+bh-20)],fill=NAVY)
        yy=by+25
        for l in lines: d.text((bx+40,yy),l,font=BUB,fill=CREAM); yy+=52
    d.text((80,1650),"Rendimenti ipotetici e costanti, al lordo di tasse e costi.",font=SM,fill=(130,135,145))
    d.text((80,1682),"Non è consulenza finanziaria.",font=SM,fill=(130,135,145))
    return im
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
  "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart","reel_stipendio_tempo.mp4"],stdin=subprocess.PIPE)
for k in range(FPS*DUR):
    p.stdin.write(frame(k/FPS).tobytes())
p.stdin.close(); p.wait()
for ts in [2,7,16,22,26]: frame(ts).resize((360,640)).save(f"snap_{ts}.jpg")
