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

Esempio rapido (Danielou con esponenti):
```bash
python3 sim.py --basenote 440 --danielou 1,2,-1 out_dan_exp
```

## Licenza
MIT License

Copyright (c) 2025 Luca Bimbi

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.
