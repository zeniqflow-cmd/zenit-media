"""Reel 22/11 'Aspettare 10 anni ti costa 140.000 €' - Zenone con voce (Kokoro, im_nicola).
Uso: python reel_aspettare10anni.py <work_dir con voce.wav, timeline.json, z_rest.png, z_point.png> <out.mp4> [snap_dir]"""
import sys, json, math, subprocess
sys.path.insert(0, __file__.rsplit('/', 3)[0] + '/tools')
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw
from lib import f, CREAM, NAVY, GOLD, SAGE

WORK, OUT = sys.argv[1], sys.argv[2]
SNAP = sys.argv[3] if len(sys.argv) > 3 else None
W, H, FPS = 1080, 1920, 30
TL = json.load(open(WORK + '/timeline.json'))
aud, SR = sf.read(WORK + '/voce.wav')
DUR = len(aud) / SR + 0.9
NF = int(DUR * FPS)

# --- numeri (ricalcolati) ---
r = 0.07 / 12
fv = lambda n: 100 * ((1 + r) ** n - 1) / r
MARCO, LUCA = fv(480), fv(360)
assert round(MARCO) == 262481 and round(LUCA) == 121997 and round(MARCO - LUCA) == 140484
V_M, V_L = 48000, 36000

# --- livello audio per fotogramma (bocca) ---
lev = np.zeros(NF)
for i in range(NF):
    a = aud[int(i / FPS * SR): int((i + 1) / FPS * SR)]
    lev[i] = np.sqrt(np.mean(a ** 2)) if len(a) else 0
lev = np.clip(lev / (np.percentile(lev[lev > 0], 90) + 1e-9), 0, 1)

SC = {s['scene']: s['start'] for s in reversed(TL)}  # inizio di ogni scena
SCEND = {s['scene']: s['end'] for s in TL}

ZR = Image.open(WORK + '/z_rest.png').convert('RGBA')
ZP = Image.open(WORK + '/z_point.png').convert('RGBA')
ZS = ZR.height / 1000.0  # px per unità svg

HOOK = f("InterDisplay-Black.otf", 150)
SUB = f("InterDisplay-Bold.otf", 74)
KICK = f("Inter-SemiBold.otf", 32)
LAB = f("Inter-SemiBold.otf", 40)
VAL = f("InterDisplay-Bold.otf", 54)
SMV = f("Inter-SemiBold.otf", 34)
SM = f("Inter-Regular.otf", 25)
BTN = f("InterDisplay-Bold.otf", 52)
GREY = (120, 126, 138)
DARKGOLD = (150, 112, 30)


def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0, min(1, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def seg(t, a, b): return ease((t - a) / (b - a))
def eur(v): return f"{int(round(v)):,}".replace(",", ".") + " €"
def eurk(v): return f"{int(round(v / 1000.0)) * 1000:,}".replace(",", ".") + " €"
def mix(c, a, bg=CREAM): return tuple(int(c[k] * a + bg[k] * (1 - a)) for k in range(3))


def words_lines(d, text, font, maxw):
    out, cur = [], []
    for w in text.split(' '):
        test = ' '.join(cur + [w])
        if cur and d.textlength(test, font=font) > maxw: out.append(cur); cur = [w]
        else: cur.append(w)
    out.append(cur); return out


def is_num(w): return any(ch.isdigit() for ch in w) or '€' in w or '%' in w


def subtitle(im, t, text, t0, y=300):
    """sottotitolo grande con 'pop' d'ingresso, numeri in oro"""
    d = ImageDraw.Draw(im)
    p = back((t - t0) / 0.22)
    lines = words_lines(d, text, SUB, 920)
    lh = 90
    layer = Image.new('RGBA', (W, len(lines) * lh + 40), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for li, ws in enumerate(lines):
        x = 80
        for w in ws:
            ld.text((x, li * lh), w, font=SUB, fill=GOLD if is_num(w) else NAVY)
            x += ld.textlength(w + ' ', font=SUB)
    s = 0.85 + 0.15 * p
    lay = layer.resize((int(layer.width * s), int(layer.height * s)))
    a = max(0, min(1, (t - t0) / 0.12))
    lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
    im.paste(lay, (int((W - lay.width) / 2), int(y + (1 - s) * 60)), lay)


def zenone(im, t, fi, x, y, h, pointing, rot=0.0):
    base = (ZP if pointing else ZR).copy()
    d = ImageDraw.Draw(base)
    # bocca: si apre col volume della voce
    o = lev[min(fi, NF - 1)]
    cx, cy = 300 * ZS, 252 * ZS
    rx = (12 + 4 * o) * ZS; ry = (2.5 + 13 * o) * ZS
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(90, 40, 34))
    if o > 0.35:
        d.rectangle([cx - rx * 0.7, cy - ry, cx + rx * 0.7, cy - ry + 3 * ZS], fill=(250, 246, 238))
    sc = h / base.height
    z = base.resize((int(base.width * sc), int(base.height * sc)), Image.LANCZOS)
    if rot: z = z.rotate(rot, resample=Image.BICUBIC, expand=True, center=(z.width // 2, z.height))
    im.paste(z, (int(x - z.width / 2), int(y - z.height)), z)
    return sc


def bars(im, t):
    d = ImageDraw.Draw(im)
    s2, s3, s4, s5 = SC[2], SC[3], SC[4], SC[5]
    base, maxh = 1430, 680
    xs = {'M': 450, 'L': 760}; bw = 240
    fade = 1 - seg(t, s5 - 0.1, s5 + 0.3)
    if fade <= 0.01: return
    # etichette età (scena 2)
    for key, name, age, col, t0 in [('M', 'Marco', 'da 22 anni', GOLD, s2), ('L', 'Luca', 'da 32 anni', SAGE, s2 + (TL_luca_start() - s2))]:
        a = seg(t, t0, t0 + 0.3)
        if a <= 0: continue
        x = xs[key]
        d.text((x + bw / 2, base + 45), name, font=LAB, fill=mix(NAVY, a * fade), anchor='mm')
        d.text((x + bw / 2, base + 92), age, font=SMV, fill=mix(GREY, a * fade), anchor='mm')
        d.line([x - 10, base, x + bw + 10, base], fill=mix(NAVY, a * fade), width=5)
    # crescita barre (scena 3) con contatore
    for key, val, col, t0 in [('M', MARCO, GOLD, s3), ('L', LUCA, SAGE, s3 + 0.5)]:
        g = seg(t, t0, t0 + 2.6)
        if g <= 0: continue
        x = xs[key]; h = maxh * val / MARCO * g
        exploded = key == 'M' and t >= s4
        if exploded:
            e = seg(t, s4, s4 + 0.7)
            hv = maxh * V_M / MARCO; hi = maxh - hv
            gap = 70 * e; shake = 6 * math.sin(t * 60) * (1 - e) if e < 1 else 0
            d.rounded_rectangle([x + shake, base - hv, x + bw + shake, base], radius=16, fill=mix(NAVY, fade))
            d.rounded_rectangle([x - 30 * e, base - hv - gap - hi, x - 30 * e + bw, base - hv - gap], radius=16, fill=mix(GOLD, fade))
            al = seg(t, s4 + 0.4, s4 + 0.9) * fade
            d.text((x + bw / 2, base - hv / 2 - 22), "versati", font=SMV, fill=mix(CREAM, al, NAVY), anchor='mm')
            d.text((x + bw / 2, base - hv / 2 + 20), eur(V_M), font=SMV, fill=mix(CREAM, al, NAVY), anchor='mm')
            yi = base - hv - gap - hi / 2
            d.text((x - 30 * e + bw / 2, yi - 26), "interessi", font=SMV, fill=mix(NAVY, al, GOLD), anchor='mm')
            d.text((x - 30 * e + bw / 2, yi + 22), "≈ " + eurk(MARCO - V_M), font=f("InterDisplay-Bold.otf", 44), fill=mix(NAVY, al, GOLD), anchor='mm')
            d.text((x - 30 * e + bw / 2, base - maxh - gap - 45), "≈ " + eurk(MARCO), font=VAL, fill=mix(NAVY, fade), anchor='mm')
        else:
            d.rounded_rectangle([x, base - h, x + bw, base], radius=16, fill=mix(col, fade))
            d.text((x + bw / 2, base - h - 45), "≈ " + eurk(val * g), font=VAL, fill=mix(NAVY, fade), anchor='mm')
        if key == 'L' and t >= s4:
            e = seg(t, s4 + 0.2, s4 + 0.8)
            hv = maxh * V_L / MARCO
            d.rounded_rectangle([x, base - hv, x + bw, base], radius=16, fill=mix(mix(NAVY, e, col), fade))
            if e > 0.3:
                al = seg(t, s4 + 0.5, s4 + 1.0) * fade
                d.text((x + bw / 2, base - hv / 2 - 20), "versati", font=SMV, fill=mix(CREAM, al, NAVY), anchor='mm')
                d.text((x + bw / 2, base - hv / 2 + 20), eur(V_L), font=SMV, fill=mix(CREAM, al, NAVY), anchor='mm')
    # differenza (dopo 'la differenza la fa il tempo')
    tdiff = TL_diff_start()
    a = seg(t, tdiff, tdiff + 0.35) * fade
    if a > 0:
        y = 535
        d.rounded_rectangle([450, y - 46, 1010, y + 46], radius=50, fill=mix(NAVY, a))
        d.text((730, y), "differenza ≈ " + eurk(MARCO - LUCA), font=SMV, fill=mix(CREAM, a, NAVY), anchor='mm')


def TL_luca_start(): return [s for s in TL if s['text'].startswith('Luca a')][0]['start']
def TL_diff_start(): return [s for s in TL if s['text'].startswith('La differenza')][0]['start']


def frame(fi):
    t = fi / FPS
    im = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16], fill=GOLD)
    s1 = SC[1]
    # ---------- HOOK (frame 1 già in movimento) ----------
    if t < s1 + 0.25:
        out = seg(t, s1 - 0.05, s1 + 0.25)
        z = 1.15 - 0.15 * back(t / 0.40)          # zoom in ingresso
        amp = 22 * max(0, 1 - t / 0.7)              # scossa
        sx, sy = amp * math.sin(t * 75), amp * math.cos(t * 61)
        layer = Image.new('RGBA', (W, 760), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        rows = [("ASPETTARE", NAVY), ("10 ANNI", NAVY), ("TI COSTA", NAVY), ("140.000 €", GOLD)]
        y = 0
        for txt, col in rows:
            fs = HOOK if col == NAVY else f("InterDisplay-Black.otf", 178)
            ld.text((W / 2, y), txt, font=fs, fill=col, anchor='ma'); y += 150 if col == NAVY else 0
        ld.rectangle([150, 470 + 180, W - 150, 470 + 196], fill=GOLD)  # sottolineatura
        lw, lh = int(W * z), int(760 * z)
        lay = layer.resize((lw, lh), Image.LANCZOS)
        if out > 0: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * (1 - out))))
        im.paste(lay, (int((W - lw) / 2 + sx), int(250 + (760 - lh) / 2 + sy)), lay)
    else:
        d.text((80, 225), "ZENONE FA I CONTI", font=KICK, fill=SAGE)
    # ---------- sottotitoli sincronizzati (scene 1+) ----------
    for s in TL:
        if s['scene'] >= 1 and s['start'] - 0.05 <= t < (s['end'] + 0.25 if s is not TL[-1] else 99):
            nxt = [x for x in TL if x['start'] > s['start']]
            if nxt and t >= nxt[0]['start'] - 0.05: continue
            subtitle(im, t, s['text'], s['start'] - 0.05)
    # ---------- scena 1: due amici, parametri ----------
    if s1 <= t < SC[3] + 0.3:
        a1 = seg(t, s1 + 1.0, s1 + 1.3) * (1 - seg(t, SC[2] - 0.2, SC[2] + 0.2))
        pills = [("100 € al mese", TL[2]['start']), ("7% l'anno", TL[3]['start']), ("stesso piano per entrambi", TL[3]['start'] + 0.6)]
        y = 620
        for lab, t0 in pills:
            a = seg(t, t0, t0 + 0.25) * (1 - seg(t, SC[2] - 0.2, SC[2] + 0.2))
            if a > 0:
                w = d.textlength(lab, font=LAB) + 80
                x0 = 470 + 40 * (1 - a)
                d.rounded_rectangle([x0, y, x0 + w, y + 86], radius=43, fill=mix(SAGE, a), outline=None)
                d.text((x0 + w / 2, y + 43), lab, font=LAB, fill=mix(NAVY, a, SAGE), anchor='mm')
            y += 115
        # due amici
        for i, (n, col) in enumerate([("M", GOLD), ("L", SAGE)]):
            a = seg(t, TL[2]['start'] + 0.15 * i, TL[2]['start'] + 0.3 + 0.15 * i) * (1 - seg(t, SC[2] - 0.2, SC[2] + 0.1))
            if a > 0:
                cx = 575 + 300 * i; cy = 1100; r = 90 * back(min(1, (t - TL[2]['start'] - 0.15 * i) / 0.3))
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mix(col, a))
                d.text((cx, cy), n, font=VAL, fill=mix(NAVY, a, col), anchor='mm')
                d.text((cx, cy + 135), ["Marco", "Luca"][i], font=LAB, fill=mix(NAVY, a), anchor='mm')
    if t >= SC[2]:
        bars(im, t)
    # ---------- CTA ----------
    if t >= SC[5]:
        a = seg(t, SC[5], SC[5] + 0.3); p = back(min(1, (t - SC[5]) / 0.35))
        bw_, bh_ = int(820 * (0.8 + 0.2 * p)), 130
        x0, y0 = (W - bw_) // 2, 640
        d.rounded_rectangle([x0, y0, x0 + bw_, y0 + bh_], radius=65, fill=mix(GOLD, a))
        d.text((W // 2, y0 + bh_ // 2), "Segui @zeni_thdigital", font=BTN, fill=mix(NAVY, a, GOLD), anchor='mm')
        a2 = seg(t, TL[-1]['start'], TL[-1]['start'] + 0.3)
        if a2 > 0:
            y1 = y0 + 170
            d.rounded_rectangle([x0, y1, x0 + bw_, y1 + bh_], radius=65, outline=mix(GOLD, a2), width=5)
            d.text((W // 2, y1 + bh_ // 2), "Salva il video", font=BTN, fill=mix(NAVY, a2), anchor='mm')
    # ---------- Zenone sempre in scena ----------
    mv = seg(t, s1 - 0.1, s1 + 0.5)
    speaking = lev[min(fi, NF - 1)]
    bob = 7 * math.sin(t * 2.4) + 5 * speaking
    if t < s1 + 0.5:
        # al centro, indica lo spettatore; spinta in avanti nei primi frame
        punch = 1 + 0.10 * (1 - ease(t / 0.5)) + 0.02 * math.sin(t * 9) * (1 - mv)
        hz = (640 * punch) * (1 - mv) + 610 * mv
        x = W / 2 * (1 - mv) + 230 * mv
        sc = zenone(im, t, fi, x, 1600 + bob, hz, pointing=True)
        if t < 1.6:  # lineette d'impatto intorno al dito
            fx = x - ZP.width * (hz / ZP.height) / 2 + 489 * ZS * (hz / ZP.height)
            fy = 1600 + bob - hz + 322 * ZS * (hz / ZP.height)
            k = (t * 3) % 1
            for ang in range(0, 360, 45):
                rr1, rr2 = 40 + 30 * k, 70 + 30 * k
                c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                d.line([fx + c * rr1, fy + s * rr1, fx + c * rr2, fy + s * rr2], fill=mix(GOLD, 1 - k), width=7)
    else:
        rot = 1.5 * math.sin(t * 1.7)
        zenone(im, t, fi, 230, 1600 + bob, 610, pointing=False, rot=rot)
    # ---------- disclaimer sempre visibile ----------
    d.text((W // 2, 1622), "Rendimenti ipotetici e costanti, al lordo di tasse e costi.", font=SM, fill=GREY, anchor='mm')
    d.text((W // 2, 1656), "Non è consulenza finanziaria.", font=SM, fill=GREY, anchor='mm')
    return im


if __name__ == '__main__':
    if SNAP:
        for ts in [0, 0.2, 0.5, 1.5, 3.0, 3.6, 5, 7.5, 10, 12, 15, 17, 18.5, 20.5, 22.5, DUR - 0.1]:
            frame(int(ts * FPS)).save(f"{SNAP}/f_{ts:05.2f}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", WORK + "/voce.wav", "-af", "apad", "-t", f"{NF / FPS:.3f}",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-profile:v", "high",
                          "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for k in range(NF):
        p.stdin.write(frame(k).tobytes())
    p.stdin.close(); p.wait()
