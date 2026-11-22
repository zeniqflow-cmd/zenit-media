# Coda di pubblicazione

Ogni post vive in `posts/AAAA-MM-GG_slug/` con:
- `01.jpg … NN.jpg` (1080x1350), `didascalia.txt`
- `stato.txt`, la prima riga è lo stato:
  - `in_attesa`: preparato dal Redattore (mattina). Esce alle 19:00 se Gianni non risponde STOP (silenzio-assenso).
  - `approvato`: ok esplicito di Gianni.
  - `bloccato`: Gianni ha risposto STOP. Non esce.
  - `pubblicato <ora> media_id <id>` / `errore: <motivo>`: scritto dal Pubblicatore.

Regole: al massimo 1 post al giorno. Il Pubblicatore (19:00) pubblica solo la cartella con la data di oggi.
