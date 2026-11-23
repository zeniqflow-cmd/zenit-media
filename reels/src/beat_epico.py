# Tema originale "epico-cosmico": organo, ticchettio d'orologio, ostinato di pianoforte in crescendo.
# Ispirato all'atmosfera di colonne sonore orchestrali; melodia e armonie originali, nessun campione esterno.
import numpy as np, wave, sys
SR=44100; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 19.0; OUT=sys.argv[1]
n=int(SR*DUR); mix=np.zeros(n); T=np.arange(n)/SR
def mtof(m): return 440*2**((m-69)/12)
def add(sig,t0,g=1.0):
    s=int(t0*SR); e=min(n,s+len(sig))
    if 0<=s<n: mix[s:e]+=g*sig[:e-s]
def organ(m,L):
    t=np.arange(int(L*SR))/SR; f=mtof(m); x=np.zeros_like(t)
    for h,a in [(0.5,0.5),(1,1),(2,0.6),(3,0.3),(4,0.25),(6,0.12),(8,0.08)]:
        x+=a*np.sin(2*np.pi*f*h*t*(1+0.0015*np.sin(2*np.pi*5*t)))
    env=np.minimum(1,t/0.9)*np.minimum(1,(L-t)/0.6).clip(0)
    return x*env*0.05
def piano(m,L=1.2):
    t=np.arange(int(L*SR))/SR; f=mtof(m)
    x=np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)+0.15*np.sin(2*np.pi*3*f*t)*np.exp(-t*5)
    return x*np.exp(-t*2.5)*np.minimum(1,t/0.004)*0.16
def tick(hi=True):
    t=np.arange(int(0.04*SR))/SR
    return np.sin(2*np.pi*(3200 if hi else 2400)*t)*np.exp(-t*180)*0.25
def boom(L=3):
    t=np.arange(int(L*SR))/SR
    return np.sin(2*np.pi*(38+20*np.exp(-t*6))*t)*np.exp(-t*1.2)*0.5
# armonia originale in La minore: Am - Fmaj7 - C/G - Esus4/E
chords=[[45,57,60,64],[41,57,60,64],[43,55,60,64],[40,56,59,64]]
L=DUR/4.0
for i,ch in enumerate(chords):
    for m in ch: add(organ(m,L+0.6),i*L, 0.7+0.25*i)
# ticchettio regolare
for k in range(int(DUR)):
    add(tick(k%2==0),k*1.0, 0.6 if k<9 else 0.9)
# ostinato di pianoforte originale (crescendo e accelerazione a metà)
mot=[69,72,76,72, 69,72,77,72]
t0=1.0; k=0
while t0<DUR-1.2:
    step=0.5 if t0<9.5 else 0.25
    g=0.4+0.6*min(1,t0/16)
    base=[0,-4,-2,-5][min(3,int(t0//L))]
    add(piano(mot[k%8]+base),t0,g); t0+=step; k+=1
# colpi gravi ai cambi scena e climax finale
for ts in (0.0,3.5,7.0,9.5,16.0): add(boom(),ts,0.8 if ts<16 else 1.2)
env=np.minimum(1,np.minimum(T/0.4,(DUR-T)/1.5))
mix*=env; mix=np.tanh(mix/np.max(np.abs(mix))*1.2); mix/=np.max(np.abs(mix)); mix*=0.89
with wave.open(OUT,"wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
