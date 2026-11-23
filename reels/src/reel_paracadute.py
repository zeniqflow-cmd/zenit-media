import sys,os,subprocess,numpy as np,wave
from PIL import Image,ImageDraw,ImageFont
F="/usr/share/fonts/opentype/inter/"
def f(n,s): return ImageFont.truetype(F+n,s)
CREAM=(245,241,232); NAVY=(31,42,68); GOLD=(201,164,76); SAGE=(143,169,152); RED=(190,80,70); GREEN=(86,150,110)
W,H=1080,1920; FPS=30; DUR=19.0
OUT=sys.argv[1]
K=f("Inter-SemiBold.otf",34); BIG=f("InterDisplay-Bold.otf",96); MID=f("InterDisplay-Bold.otf",70); B=f("Inter-Regular.otf",46); BB=f("Inter-SemiBold.otf",48); SM=f("Inter-Regular.otf",28); NUM=f("InterDisplay-Bold.otf",150)
def ease(x): x=max(0.0,min(1.0,x)); return 1-(1-x)**3
def wrap(d,t,font,maxw):
    out=[];c=""
    for w in t.split(" "):
        x=(c+" "+w).strip()
        if d.textlength(x,font=font)<=maxw: c=x
        else: out.append(c); c=w
    out.append(c); return out
def txt(d,x,y,t,font,fill,maxw=920,lh=1.15):
    for l in wrap(d,t,font,maxw): d.text((x,y),l,font=font,fill=fill); y+=int(font.size*lh)
    return y
def fadein(im,a):
    return im if a>=1 else Image.blend(Image.new("RGB",im.size,im.getpixel((5,500))),im,a)
PARA=[("Fondo emergenze","3-6 mesi di spese sul conto, fuori dalla borsa."),
      ("Niente leva","Con i debiti un calo diventa un disastro."),
      ("PAC continuo","Quando scende, compri più quote."),
      ("Ribilancia","Una volta l'anno torni alle percentuali scelte.")]
def frame(t):
    dark = t<9.5 or t>=16
    bg=NAVY if dark else CREAM; fg=CREAM if dark else NAVY; sub=(200,208,220) if dark else (80,90,110)
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,int(W*min(1,t/DUR))*0+16],fill=GOLD)
    d.rectangle([0,16,int(W*t/DUR),24],fill=SAGE)
    if t<3.5:
        a=ease(t/0.4)
        d.text((80,300),"BORSA · 5 NOVEMBRE 2026",font=K,fill=GOLD)
        y=txt(d,80,370,"Nasdaq in un giorno:",MID,fg)
        v=-4.9*ease((t-0.3)/1.2)
        d.text((80,y+40),f"{v:+.1f}%".replace(".",",").replace("-","−"),font=NUM,fill=RED)
        h=int(520*ease((t-0.3)/1.2)); d.rectangle([700,900,900,900+h],fill=RED)
        txt(d,80,1150,"Sui social: “è il crollo”.",B,sub,560)
        return fadein(im,a)
    if t<7:
        tt=t-3.5
        d.text((80,300),"BORSA · OGGI, 23 NOVEMBRE",font=K,fill=GOLD)
        y=txt(d,80,370,"Il tech torna a correre. STMicroelectronics:",MID,fg)
        v=9.5*ease((tt-0.2)/1.2)
        d.text((80,y+40),f"+{v:.1f}%".replace(".",","),font=NUM,fill=GREEN)
        h=int(520*ease((tt-0.2)/1.2)); d.rectangle([700,1420-h,900,1420],fill=GREEN)
        txt(d,80,1150,"In un solo giorno, a Piazza Affari.",B,sub,560)
        return fadein(im,ease(tt/0.3))
    if t<9.5:
        tt=t-7
        y=txt(d,80,560,"Chi ha venduto nel panico",BIG,fg)
        if tt>0.9: txt(d,80,y+30,"si è perso il rimbalzo.",BIG,GOLD)
        return fadein(im,ease(tt/0.3))
    if t<16:
        tt=t-9.5
        d.text((80,260),"COME TUTELARSI",font=K,fill=SAGE)
        txt(d,80,320,"4 paracadute prima del prossimo calo",MID,NAVY)
        y=620
        for i,(a,b) in enumerate(PARA):
            p=ease((tt-0.3-i*1.3)/0.5)
            if p<=0: break
            x=80+int((1-p)*120)
            d.rounded_rectangle([x,y,x+920,y+200],radius=28,fill=(255,255,255),outline=(214,208,195),width=3)
            d.ellipse([x+30,y+50,x+130,y+150],fill=GOLD); d.text((x+80,y+100),str(i+1),font=MID,fill=NAVY,anchor="mm")
            d.text((x+160,y+38),a,font=BB,fill=NAVY)
            txt(d,x+160,y+100,b,f("Inter-Regular.otf",36),(80,90,110),740,1.2)
            y+=230
        return fadein(im,ease(tt/0.3))
    tt=t-16
    y=txt(d,80,620,"Il mercato sale e scende.",MID,CREAM)
    y=txt(d,80,y+20,"Il tuo piano no.",BIG,GOLD)
    d.rounded_rectangle([80,y+80,W-80,y+200],radius=60,outline=GOLD,width=4)
    d.text((W//2,y+140),"Salva e segui @zeni_thdigital",font=BB,fill=CREAM,anchor="mm")
    return fadein(im,ease(tt/0.3))
def foot(im,dark):
    d=ImageDraw.Draw(im); c=(150,160,180) if dark else (130,130,130)
    d.text((80,1640),"Fonti: Milano Finanza 5/11/2026; QuiFinanza 23/11/2026.",font=SM,fill=c)
    d.text((80,1720),"I rendimenti passati non garantiscono quelli futuri.",font=SM,fill=c)
    d.text((80,1760),"Non è consulenza finanziaria.",font=SM,fill=c)
    d.text((80,1820),"Budget Zen",font=f("InterDisplay-SemiBold.otf",34),fill=c)
    return im
# audio: jingle originale (pad + arpeggio + basso), sintetizzato qui
SR=44100; n=int(SR*DUR); tA=np.arange(n)/SR; out=np.zeros(n)
def note(m): return 440*2**((m-69)/12)
chords=[[62,66,69],[59,62,66],[55,59,62],[57,61,64]]*3  # D Bm G A
cl=DUR/ (len(chords)) 
for i,ch in enumerate(chords):
    a=int(i*cl*SR); b=min(n,int((i+1)*cl*SR)+SR//4); tt=np.arange(b-a)/SR
    env=np.minimum(1,tt/0.4)*np.minimum(1,(b-a)/SR-tt+0.05)
    for m in ch:
        for det in (-0.08,0.08): out[a:b]+=0.05*env*np.sin(2*np.pi*note(m+det)*tt)
    bass=note(ch[0]-24); out[a:b]+=0.10*env*np.sin(2*np.pi*bass*tt)
    step=cl/4
    for k,m in enumerate(ch+[ch[0]+12]):
        s=int((i*cl+k*step)*SR); e=min(n,s+int(0.9*SR)); te=np.arange(e-s)/SR
        out[s:e]+=0.07*np.exp(-te*4)*(np.sin(2*np.pi*note(m+12)*te)+0.3*np.sin(2*np.pi*note(m+24)*te))
# colpo di timpano ai cambi scena
for ts in (0,3.5,7,9.5,16):
    s=int(ts*SR); e=min(n,s+int(0.6*SR)); te=np.arange(e-s)/SR
    out[s:e]+=0.25*np.exp(-te*7)*np.sin(2*np.pi*55*te*(1+0.5*np.exp(-te*20)))
fade=np.minimum(1,np.minimum(tA/0.3,(DUR-tA)/1.2)); out*=fade
out=out/np.max(np.abs(out))*0.8
with wave.open("/tmp/jingle.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes())
p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","/tmp/jingle.wav","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",OUT],stdin=subprocess.PIPE)
for i in range(int(DUR*FPS)):
    t=i/FPS; im=frame(t); im=foot(im, t<9.5 or t>=16)
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait()
