# SIM - Sistemi di Intonazione Musicale

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Generatore di rapporti/parametri per la costruzione di tabelle di accordatura (ad es. cpstun per Csound),
con esportazione di tabelle di confronto (12TET e serie armonica) e opzionale export in formato `.tun` (AnaMark TUN).

Caratteristiche principali:
- Temperamento equabile (ET) con conversione frazione↔cents;
- Sistema geometrico su generatore con riduzione all’ottava opzionale;
- Sistema naturale (4:5:6) e sistema Danielou (sottoinsieme o griglia completa);
- Esportazione tabelle `.txt`/`.xlsx`, file `.csd` con tabella cpstun (GEN -2), e `.tun`.
- Confronto 12TET configurabile: `--compare-fund` per la fondamentale e `--compare-tet-align {same,nearest}` per l’allineamento.
- File `.txt` con colonne allineate a larghezza fissa per etichette e valori.

## Licenza
MIT License

Copyright (c) 2025 Luca Bimbi

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.
