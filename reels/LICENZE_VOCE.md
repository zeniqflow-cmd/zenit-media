# Licenze della voce di Zenone

Verificato il 19/11/2026 per il Reel `2026-11-22_aspettare10anni.mp4`.

| Componente | Cosa fa | Licenza | Uso commerciale |
|---|---|---|---|
| **Kokoro-82M v1.0** (hexgrad) – pesi del modello TTS | genera la voce | **Apache 2.0** (model card: https://huggingface.co/hexgrad/Kokoro-82M) | Sì |
| **Voce `im_nicola`** (italiano, maschile) | timbro di Zenone | inclusa nel pacchetto voci di Kokoro-82M v1.0, stessa licenza **Apache 2.0** | Sì |
| `kokoro-onnx` 0.6.1 (thewh1teagle) – file `kokoro-v1.0.onnx` / `voices-v1.0.bin` | esegue il modello in ONNX | MIT (libreria), pesi convertiti da Kokoro-82M Apache 2.0 | Sì |
| `phonemizer` + espeak-ng | trasforma il testo in fonemi | GPL-3.0 | Sì: è solo uno strumento usato in locale; la GPL riguarda il software, non l'audio prodotto, e il software non viene distribuito |

Conclusione: **la voce si può usare in contenuti commerciali** (Reel, sponsorizzate). Apache 2.0 non richiede di citare il modello nel video; per correttezza conserviamo questo file nel repo.

Note
- La voce è sintetica e non imita una persona reale.
- Hash SHA-256 dei file usati: `kokoro-v1.0.onnx` 7d5df8ec…3636a6c5, `voices-v1.0.bin` bca610b8…29f1fbf7d.
- Rigenerare: `python reels/src/voce_kokoro.py <cartella_modello> <out>` poi `python reels/src/reel_aspettare10anni.py <out> reels/2026-11-22_aspettare10anni.mp4` (prima `reels/src/zenone_varianti.py reels/zenone.svg <out>`).
