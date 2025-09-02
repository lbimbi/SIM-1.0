# SIM - Sistemi di Intonazione Musicale

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Generatore di rapporti/parametri per la costruzione di tabelle di accordatura (ad es. cpstun per Csound),
con esportazione di tabelle di confronto (12TET, serie armonica e serie subarmonica) e opzionale export in formato `.tun` (AnaMark TUN).

Caratteristiche principali:
- Temperamento equabile (ET) con conversione frazione↔cents;
- Sistema geometrico su generatore con riduzione all’ottava opzionale;
- Sistema naturale (4:5:6) e sistema Danielou (sottoinsieme, griglia completa o esponenti a,b,c);
- Esportazione tabelle `.txt`/`.xlsx`, file `.csd` con tabella cpstun (GEN -2), e `.tun`.
- Confronto configurabile (12TET, armonica e subarmonica): `--compare-fund` (default=basenote; può essere usato senza argomento), `--compare-tet-align {same,nearest}`, `--subharm-fund` (default: A5). Colonne TET_Hz e TET_Note in ogni riga; ordinamento crescente per tutte le colonne, cut‑off: armoniche ≤ 10 kHz e subarmoniche ≥ 16 Hz; evidenziazione < 17 Hz solo nei TXT (in Excel restano i riempimenti colore). Flag `--midi-truncate` per troncamento al range MIDI 0..127.
- File `.txt` con colonne allineate a larghezza fissa per etichette e valori.
- Le tabelle cpstun nel file `.csd` sono scritte con i ratio in ordine crescente.
- File `.tun` (AnaMark TUN): 128 righe `Note n=... cents` in ordine 0→127, con valori in cents assoluti riferiti a 8.1757989156437073336 Hz (riferimento AnaMark, A=440). Il segmento personalizzato derivato dai ratios è ordinato in modo crescente. Per impostazione predefinita i valori sono arrotondati a due decimali; con `--tun-integer` vengono esportati come interi (senza decimali).
- Sistema geometrico: `INTERVAL` come intero senza suffisso è interpretato in cents (es. 700 → 700c); accetta anche il suffisso `c` e, per indicare un rapporto, usare float o frazione (es. 2.0 o 2/1).

Esempio rapido (Danielou con esponenti):
```bash
python3 SIM-2NV.py --basenote 440 --danielou 1,2,-1 out_dan_exp
```

Nota su esponenti negativi: se il primo valore (a) è negativo, usa la sintassi con "=" e virgolette per evitare che la shell/argparse lo interpreti come un'opzione.
Esempio robusto:
```bash
python3 SIM-2NV.py --danielou="-1,2,0" out_dan_neg
```

Esempio multi-terna (triplette multiple, inclusa una con a negativo):
```bash
python3 SIM-2NV.py \
  --danielou="a,b,c" \
  --danielou="a,b,c" \
  --danielou="-a,b,c" \
  out_file
```

## SIM-2NV.py
`SIM-2NV.py` è una variante dell'utility orientata alla generazione di sistemi e file di supporto con un set di opzioni ampliato e una pipeline di export completa (cpstun, .tun, tabelle TXT/XLSX, confronti). Per i dettagli completi vedere il manuale dedicato: [manual-2nv.md](manual-2nv.md).

Uso rapido:
```bash
# default 12-TET su ottava, genera out.csd, out_system.txt, out_compare.txt
python3 SIM-2NV.py out

# esporta anche AnaMark .tun
python3 SIM-2NV.py --export-tun out

# .tun con cents interi (arrotondamento al valore più vicino)
python3 SIM-2NV.py --export-tun --tun-integer out_int

# sistema Danielou (esponenti); attenzione agli esponenti negativi
python3 SIM-2NV.py --danielou "-1,2,0" out_dan

# progressione geometrica: generatore 3/2, 12 passi, intervallo 2/1 (ottava)
python3 SIM-2NV.py --geometric 3/2 12 2/1 out_geo
```

Note:
- Opzioni di confronto disponibili: `--compare-fund`, `--compare-tet-align {same,nearest}`. Vedi manuale per dettagli su tagli e ordinamenti delle tabelle.
- Per estendere l'ambitus oltre una singola ripetizione usare `--span N`.
- cpstun (GEN -2): `--interval-zero` forza `interval=0` usando la serie non ripetuta; in assenza, se i ratios sono in [1,2] viene scelto `interval=2.0`, altrimenti `0.0`.
- Range MIDI: `--midi-truncate` tronca oltre 128 note; senza truncation il programma adatta `basekey` se necessario.
- Export Excel (`*.xlsx`): richiede `openpyxl`; se mancante, vengono creati solo i `.txt`. 

## Licenza
MIT License

Copyright (c) 2025 Luca Bimbi

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.
