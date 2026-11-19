"""Genera la voce di Zenone con Kokoro-82M (kokoro-onnx), voce im_nicola, italiano.
Uso: python voce_kokoro.py <cartella_modello> <out_dir>
Ogni pezzo di sottotitolo è sintetizzato a parte e poi unito: così audio e sottotitoli sono allineati al campione."""
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
# (testo parlato, testo a schermo, pausa dopo in secondi)
CHUNKS = [
 [("Aspettare dieci anni ti costa centoquarantamila euro.", "ASPETTARE 10 ANNI TI COSTA 140.000 €", 0.30)],
 [("Non ci credi?", "Non ci credi?", 0.12),
  ("Due amici, cento euro al mese,", "Due amici, 100 € al mese,", 0.06),
  ("sette per cento l'anno.", "7% l'anno.", 0.28)],
 [("Marco inizia a ventidue anni.", "Marco inizia a 22 anni.", 0.12),
  ("Luca a trentadue.", "Luca a 32.", 0.28)],
 [("A sessantadue anni, Marco ha circa duecentosessantaduemila euro.", "A 62 anni, Marco ha circa 262.000 €.", 0.14),
  ("Luca, centoventiduemila.", "Luca, 122.000 €.", 0.30)],
 [("Luca ha versato solo dodicimila euro in meno.", "Luca ha versato solo 12.000 € in meno.", 0.16),
  ("La differenza la fa il tempo.", "La differenza la fa il tempo.", 0.32)],
 [("Segui la pagina:", "Segui la pagina:", 0.10),
  ("ogni settimana un conto che nessuno ti fa.", "ogni settimana un conto che nessuno ti fa.", 0.0)],
]
SPEED = 1.22
if __name__ == "__main__":
    mdir, out = sys.argv[1], sys.argv[2]
    k = Kokoro(mdir + "/kokoro-v1.0.onnx", mdir + "/voices-v1.0.bin")
    sr = 24000; parts = []; t = 0.0; timeline = []
    for si, sent in enumerate(CHUNKS):
        for spoken, shown, pause in sent:
            a, sr = k.create(spoken, voice="im_nicola", speed=SPEED, lang="it")
            idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0] - 120): idx[-1] + 1200]
            timeline.append({"scene": si, "start": round(t, 3), "end": round(t + len(a) / sr, 3), "text": shown, "spoken": spoken})
            parts += [a, np.zeros(int(pause * sr), dtype=a.dtype)]; t += len(a) / sr + pause
    audio = np.concatenate(parts)
    audio = audio / max(1e-6, np.abs(audio).max()) * 0.89
    sf.write(out + "/voce.wav", audio, sr)
    json.dump(timeline, open(out + "/timeline.json", "w"), ensure_ascii=False, indent=1)
    print(round(len(audio) / sr, 2), "s")
