from PIL import Image, ImageDraw, ImageFont
import os, zipfile
W,H=1080,1350
SAGE=(143,169,152); CREAM=(245,241,232); NAVY=(31,42,68); GOLD=(201,164,76); WHITE=(255,255,255); RED=(190,80,70); LINE=(214,208,195)
F="/usr/share/fonts/opentype/inter/"
def f(n,s): return ImageFont.truetype(F+n,s)
def wrap(d,t,font,maxw):
    out=[]
    for para in t.split("\n"):
        ws=para.split(); c=""
        for w in ws:
            x=(c+" "+w).strip()
            if d.textlength(x,font=font)<=maxw: c=x
            else: out.append(c); c=w
        out.append(c)
    return out
def block(d,x,y,t,font,fill,maxw,lh=1.3):
    for l in wrap(d,t,font,maxw): d.text((x,y),l,font=font,fill=fill); y+=int(font.size*lh)
    return y
KICK=f("Inter-SemiBold.otf",30); HOOK=f("InterDisplay-Bold.otf",100); T=f("InterDisplay-Bold.otf",80); B=f("Inter-Regular.otf",46); BB=f("Inter-SemiBold.otf",44); S=f("Inter-Medium.otf",30); MONO=f("Inter-Medium.otf",46)
def frame(i,n,dark=False):
    bg=NAVY if dark else CREAM; fg=CREAM if dark else NAVY
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,16],fill=GOLD if dark else SAGE)
    d.text((80,H-100),"Budget Zen",font=f("InterDisplay-SemiBold.otf",32),fill=fg)
    # dots
    x0=W-80-(n*26)
    for k in range(n): d.ellipse([x0+k*26,H-88,x0+k*26+12,H-76],fill=(GOLD if k==i else (90,100,120) if dark else LINE))
    return im,d,fg
def slide_hook(kicker,title,sub,i,n):
    im,d,fg=frame(i,n,True)
    d.text((80,260),kicker.upper(),font=KICK,fill=GOLD)
    y=block(d,80,320,title,HOOK,CREAM,920,1.12); y+=40
    y=block(d,80,y,sub,B,(200,208,220),920)
    d.text((W-80,H-200),"Scorri  →",font=BB,fill=GOLD,anchor="ra")
    return im
def slide(label,title,body,i,n,box=None,boxcolor=NAVY):
    im,d,fg=frame(i,n)
    d.text((80,250),label.upper(),font=KICK,fill=SAGE)
    y=block(d,80,305,title,T,NAVY,920,1.15); y+=45
    y=block(d,80,y,body,B,NAVY,920); y+=40
    if box:
        lines=wrap(d,box,MONO,840); h=len(lines)*int(MONO.size*1.35)+70
        d.rounded_rectangle([80,y,W-80,y+h],radius=28,fill=boxcolor)
        yy=y+35
        for l in lines: d.text((120,yy),l,font=MONO,fill=CREAM); yy+=int(MONO.size*1.35)
    return im
def slide_cta(title,body,i,n):
    im,d,fg=frame(i,n,True)
    y=block(d,80,300,title,T,CREAM,920,1.15); y+=40
    y=block(d,80,y,body,B,(200,208,220),920); y+=60
    for lab in ["Salva il carosello","Mandalo a chi ne ha bisogno","Segui @zeni_thdigital"]:
        d.rounded_rectangle([80,y,W-80,y+100],radius=50,outline=GOLD,width=3)
        d.text((W//2,y+50),lab,font=BB,fill=CREAM,anchor="mm"); y+=125
    return im
def save(name,slides,caption):
    os.makedirs(name,exist_ok=True)
    for k,s in enumerate(slides,1): s.convert("RGB").save(f"{name}/{k:02d}.jpg",quality=92)
    open(f"{name}/didascalia.txt","w",encoding="utf-8").write(caption)
    with zipfile.ZipFile(f"{name}.zip","w") as z:
        for fn in sorted(os.listdir(name)): z.write(f"{name}/{fn}",f"{name}/{fn}")
    prev=Image.new("RGB",(len(slides)*270,338))
    for k,s in enumerate(slides): prev.paste(s.resize((270,338)),(k*270,0))
    prev.save(f"prev_{name}.png")

