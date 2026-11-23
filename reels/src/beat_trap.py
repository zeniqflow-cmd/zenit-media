# Beat originale stile "trap/money" sintetizzato da zero (nessun campione esterno).
import numpy as np, wave, sys
SR=44100; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 19.0; OUT=sys.argv[1]
n=int(SR*DUR); mix=np.zeros(n); rng=np.random.default_rng(7)
BPM=140; beat=60/BPM; bar=4*beat
def add(sig,t0,g=1.0):
    s=int(t0*SR); e=min(n,s+len(sig))
    if s<n: mix[s:e]+=g*sig[:e-s]
def mtof(m): return 440*2**((m-69)/12)
def kick():
    t=np.arange(int(0.35*SR))/SR; f=50+120*np.exp(-t*35)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)
def b808(m,L):
    t=np.arange(int(L*SR))/SR; f=mtof(m)*(1+0.6*np.exp(-t*40))
    x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.minimum(1,np.exp(-(t-L+0.08).clip(0)*30))
    return np.tanh(2.2*x)*0.9
def clap():
    t=np.arange(int(0.25*SR))/SR; x=rng.standard_normal(len(t))
    env=np.exp(-t*25)+0.6*np.exp(-((t-0.012)*90)**2)+0.5*np.exp(-((t-0.024)*90)**2)
    x=np.diff(np.concatenate([[0],x]))  # passa-alto grezzo
    return x*env*0.5
def hat(L=0.05,open_=False):
    t=np.arange(int((0.25 if open_ else L)*SR))/SR; x=rng.standard_normal(len(t))
    x=np.diff(np.diff(np.concatenate([[0,0],x])))
    return x*np.exp(-t*(12 if open_ else 70))*0.12
def bell(m,L=0.6):
    t=np.arange(int(L*SR))/SR; f=mtof(m)
    return (np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*2*f*t)+0.25*np.sin(2*np.pi*3.01*f*t))*np.exp(-t*6)*0.18
def coin():  # "ka-ching" sintetico
    t=np.arange(int(0.5*SR))/SR
    return (np.sin(2*np.pi*2637*t)+np.sin(2*np.pi*3520*t)*(t>0.06))*np.exp(-t*8)*0.15
# progressione Do minore: Cm Ab Eb G (radici 808)
roots=[36,32,39,31]; arps=[[60,63,67,72],[56,60,63,68],[63,67,70,75],[55,59,62,67]]
nb=int(np.ceil(DUR/bar))
for b in range(nb):
    t0=b*bar; ch=b%4; intro = b==0
    # melodia pluck "da ricco": arpeggio in sedicesimi puntati
    pat=[0,2,1,3,2,1,3,0]
    for k,p in enumerate(pat): add(bell(arps[ch][p]+12),t0+k*beat/2,0.9)
    if intro: 
        for k in range(8): add(hat(),t0+k*beat/2,0.6)
        continue
    add(kick(),t0); add(kick(),t0+2.5*beat,0.8)
    add(b808(roots[ch],bar*0.9),t0,0.55)
    add(clap(),t0+2*beat)
    # hi-hat in ottavi con rullate da 1/16 e terzine
    for k in range(8):
        if k==7 and b%2==1:
            for r in range(3): add(hat(),t0+k*beat/2+r*beat/6,0.9)
        elif k==3:
            for r in range(2): add(hat(),t0+k*beat/2+r*beat/4)
        else: add(hat(),t0+k*beat/2)
    add(hat(open_=True),t0+3.5*beat,0.7)
for ts in (0.05,3.5,7,9.5,16): add(coin(),ts,1.0)
env=np.minimum(1,np.minimum(np.arange(n)/SR/0.05,(DUR-np.arange(n)/SR)/1.0))
mix*=env; mix=np.tanh(mix/np.max(np.abs(mix))*1.4); mix/=np.max(np.abs(mix)); mix*=0.89
with wave.open(OUT,"wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
