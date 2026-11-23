# Regole operative ZenithDigital (lette da tutte le attività automatiche)

## Squadra
- Analista (22:23 lun-ven, post del giorno dopo), Redattore (7:17, controllo e weekend), Regista (12:37 mar/gio/sab, Reel), Revisore indipendente (18:31, può bloccare il post), Community manager (13:13 e 21:13, risposte ai commenti), Stratega marketing (21:07 ogni sera).
- PRIMA di lavorare, ognuno legge backlog/MARKETING.md e applica le direttive dello Stratega. Dopo il lavoro, ognuno aggiunge in fondo a backlog/DIARIO_SQUADRA.md una riga: data, ruolo, cosa ha fatto, un dubbio o una proposta per gli altri.

## Pubblico e tono
- Investitori e risparmiatori italiani, soprattutto giovani. Concetti di alta finanza spiegati in modo semplice: forti ma chiari. Mai consigli "da bambini".
- Numeri sempre ricalcolati in Python; scenari ipotetici dichiarati come tali. Mai promesse di guadagno ("da 10k a 100k" solo come esempio matematico con ipotesi e rischi esplicitati).

## Ogni post (carosello o Reel)
- Didascalia con DOMANDA da commentare (1 riga, specifica, facile) + "Commenta ZEN e ti mando in privato il regalo: <titolo PDF>".
- Regalo: PDF didattico specifico del post, generato con `python3 tools/regalo_pdf.py regali/src_<data>_<slug>.txt regali/<data>_<slug>.pdf`, aggiunto IN CIMA alla tabella di regali/README.md.
- Hashtag: 8-10, tutti con #.
- Chiusura: "Esempio didattico. Non è consulenza finanziaria."

## Reel (formato omino)
- Stile Zenith: blu notte #1F2A44, crema #F5F1E8, oro #C9A44C, font Inter. Modello: reels/src/reel_costi_fondo_beat.py.
- Due personaggi, stessa situazione, una sola differenza; emozioni visibili (testa bassa + nuvola / salto con braccia alzate); contatori in movimento; sottotitoli integrati; 25-30 s; 1080x1920 con traccia audio muta.
- Brano scelto: "C'est La Vie" (Jennah Bell), aggiunto da Gianni dall'app. Griglia ritmica: vedi backlog/MARKETING.md (se manca, usa giri regolari da 1,7 s finché non viene misurata).
- Il brano lo aggiunge Gianni dall'app: il Reel NON si pubblica in automatico, si manda a Gianni con notifica.

## Pagine dove Gianni commenta (10 min al giorno, 5 commenti utili, post usciti da meno di un'ora)
@economiaxfinanza · @pecuniami · @finvestire · @startingfinance
