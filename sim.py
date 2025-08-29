#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIM - Sistemi intonazione musicale
Copyright (c) 2025 Luca Bimbi
Licensed under the MIT License - see LICENSE file for details

Nome programma: SIM - Sistemi intonazione musicale
Versione: 1.0
Autore: LUCA BIMBI
Data: 2025-08-29

Descrizione
-----------
Generatore di parametri/rapporti utili alla costruzione di tabelle di accordatura
(per esempio per cpstun in Csound). Supporta due modalità principali:

1) Temperamento equabile (ET)
   - Calcolo del rapporto della radice per un temperamento equabile generico
     specificando l'indice della radice (es. 12 per 12-TET) e l'ampiezza dell'ottava
     in cents (es. 1200), oppure una frazione razionale (es. 3/2) da convertire in cents.
   - Esempio: -et 12 1200

2) Sistema geometrico su generatore
   - Genera una progressione geometrica a partire da un generatore (es. 3/2) per un numero
     di passi desiderato, con riduzione all'ottava attiva di default (ricondotti in [1, 2)).
   - Opzione --no-reduce per mantenere i rapporti non ridotti (crescenti senza ricondurli in ottava).
   - Esempio: --geometric 3/2 12

3) Sistema di intonazione naturale (4:5:6)
   - Rapporti generati con formula ((3/2)^a) * ((5/4)^b).
   - Intervalli esplorati variando a in [-A_MAX...A_MAX] e b in [-B_MAX...B_MAX].
   - Esempio: --natural 3 3

4) Sistema Danielou
   - Formula: ((6/5)^a) * (3/2)^b * 2^c, con c usato per la riduzione in ottava.
   - Default: sottoinsieme a partire dalla tonica, tre terze minori armoniche successive,
     tre seste maggiori armoniche successive e l'asse delle quinte (a=0, b=-5..5).
   - Opzione --danielou-all per includere la griglia completa a∈[-3..3], b∈[-5..5] (fino a 53 rapporti).
   - Opzioni esponenti: --danielou-a INT --danielou-b INT --danielou-c INT per generare un rapporto specifico.

Input e parametri principali
---------------------------
- --basenote: nota di riferimento come nome (es. "A4", "F#2") oppure frequenza in Hz (float).
- --diapason: diapason in Hz usato per convertire i nomi di nota in Hz (default: 440).
- --basekey: nota base (MIDI key) per tabella cpstun; attualmente è un parametro informativo
  lasciato per compatibilità d'uso (default: 60 = C4).
- -et INDEX Cents|Frazione: imposta l'ET; i cents possono essere interi o una frazione (es. 3/2).
- --geometric GEN STEPS: imposta il sistema geometrico (GEN può essere intero, frazione o float;
  STEPS è il numero di passi, > 0). Riduzione all'ottava attiva di default.
- --natural A_MAX B_MAX: sistema naturale 4:5:6 con ((3/2)^a)*((5/4)^b), a∈[-A_MAX...A_MAX], b∈[-B_MAX...B_MAX].
- --danielou: genera il sistema Danielou (sottoinsieme predefinito); aggiungi --danielou-all per la griglia completa (fino a 53 rapporti).
- --no-reduce: disattiva la riduzione all'ottava in modalità generazione (default: riduci).
- output_file: nome base del file di output; verrà creato/aggiornato "<output_file>.csd" con tabelle cpstun (righe 'f') di tipo GEN -2 contenenti i rapporti (ratios) generati.

Note su frazioni e cents
------------------------
- Se per -et vengono passati i cents come frazione razionale (Fraction), questa viene convertita in cents
  tramite il logaritmo naturale secondo la scala di Ellis.
- Conversioni disponibili: ratio -> cents (fraction_to_cents) e cents -> ratio approssimato (cents_to_fraction).

Esempi d'uso
------------
- Geometrico con riduzione in ottava (default):
  python3 sim.py --basekey 60 --basenote 440 --geometric 3/2 12 out

- Geometrico senza riduzione in ottava:
  python3 sim.py --basekey 60 --basenote 440 --geometric 3/2 5 --no-reduce out2

- Sistema naturale 4:5:6 (a, b in [-3..3]):
  python3 sim.py --basekey 60 --basenote 440 --natural 3 3 out_nat

- Sistema Danielou (sottoinsieme):
  python3 sim.py --basekey 60 --basenote 440 --danielou out_dan

- Sistema Danielou (griglia completa, fino a 53 rapporti):
  python3 sim.py --basekey 60 --basenote 440 --danielou-all out_dan_all

- Temperamento equabile 12-TET (ottava 1200 cents):
  python3 sim.py --basekey 60 --basenote 440 -et 12 1200 out_et

Output
------
- Stampa a video le frequenze calcolate per ciascun passo.
- Scrive/aggiorna un file "<output_file>.csd" aggiungendo una riga di score per cpstun:
  una f‑tabella di tipo GEN -2 che contiene i seguenti campi all'interno della lista dati:
  [numgrades, interval, basefreq, basekey, r1, r2, ...].
  - numgrades = numero di rapporti generati;
  - interval = 2.0 se tutti i rapporti sono in [1,2), altrimenti 0.0 se non definibile;
  - basefreq = frequenza assoluta associata a basekey (Hz);
  - basekey = nota MIDI di riferimento.
  Ogni esecuzione sullo stesso file aggiunge una nuova tabella con numero (f_max + 1). I valori r1..rn sono i
  rapporti (unitless) rispetto a basefreq; se i rapporti superano l'ottava, interval verrà impostato a 0.0 e i
  rapporti saranno riportati così come sono.
- Esporta tabelle del sistema generato (Step, MIDI, Ratio, Hz) in "<output_file>_system.txt" e, se disponibile openpyxl,
  anche "<output_file>_system.xlsx".
- Esporta tabelle di confronto con 12TET e con la serie armonica (incluse colonne DeltaHz) in
  "<output_file>_compare.txt" e, se disponibile openpyxl, anche "<output_file>_compare.xlsx"
  disponendo valori vicini affiancati (Custom accanto a Harmonic) e usando colori distinti
  (rosso per Custom, verde per Harmonics, blu per TET), con evidenziazione quando le differenze sono molto piccole.
- Opzionale: esporta un file ".tun" (AnaMark TUN) con la mappatura assoluta di tutte le 128 note MIDI
  usando --export-tun. Le altezze dei passi generati vengono assegnate a partire da basekey,
  con frequenze assolute calcolate come basefrequency * ratio; le altre note vengono riempite
  in 12TET relativo alla stessa basefrequency.

"""

from __future__ import annotations

import argparse
import sys
import math
from fractions import Fraction
import re
import os
from typing import Iterable

# Metadati di modulo
__program_name__ = "SIM"
__version__ = "1.1"
__author__ = "LUCA BIMBI"
__date__ = "2025-08-29"

# Fattore di conversione per passare da logaritmo naturale a cents (scala di Ellis)
# 1 ottava = 1200 cents, e log base 10 => si usa 1200 / log(2)
ELLIS_CONVERSION_FACTOR = 1200 / math.log(2)

# pattern REGEX per determinare funzione e numero tabella in un file esistente
PATTERN = re.compile(r"\bf\s*(\d+)\b")
# \b bonduary; lettera f \s* spazi; (\d+) cifra o cifre

# Tolleranza per confronto floating dei rapporti
RATIO_EPS = 1e-9

def is_fraction_type(value) -> bool:
    """Ritorna True se value è una frazione (fractions.Fraction).

    Utile per distinguere quando l'utente fornisce un rapporto razionale
    invece di un intero per i cents.
    """
    return isinstance(value, Fraction)


def fraction_to_cents(ratio: Fraction) -> int:
    """Converte un rapporto razionale (Fraction) in cents.

    Formula: cents = round(ln(numeratore/denominatore) * 1200 / ln(2)).
    """
    decimal: float = math.log(ratio.numerator / ratio.denominator)
    cents = round(decimal * ELLIS_CONVERSION_FACTOR)
    return cents


def cents_to_fraction(cents: float) -> Fraction:
    """Converte una quantità di cents in un rapporto razionale approssimato.

    Usa l'antilog e poi costruisce una Fraction dal float risultante.
    """
    return Fraction(math.exp(cents / ELLIS_CONVERSION_FACTOR))


def normalize_ratios(ratios: Iterable[float | Fraction], reduce_octave: bool = True) -> list[float]:
    """Normalizza una lista di rapporti:
    - Opzionalmente riduce nell'ottava [1, 2) (default True)
    - Elimina duplicati con tolleranza RATIO_EPS
    - Ordina in modo crescente
    Restituisce una lista di float.
    """
    processed: list[float] = []
    seen: list[float] = []
    for r in ratios:
        v = r
        if reduce_octave:
            v = reduce_to_octave(v)
        v_float = float(v)
        # dedup con tolleranza
        duplicate = False
        for s in seen:
            if abs(v_float - s) <= RATIO_EPS:
                duplicate = True
                break
        if not duplicate:
            seen.append(v_float)
            processed.append(v_float)
    processed.sort()
    return processed


def pow_fraction(fr: Fraction | float, k: int) -> Fraction | float:
    """Eleva una Fraction/float ad un esponente intero (anche negativo)."""
    if isinstance(fr, Fraction):
        return fr ** int(k)
    else:
        return float(fr) ** int(k)


def build_natural_ratios(a_max: int, b_max: int, reduce_octave: bool = True) -> list[float]:
    """Genera rapporti del sistema naturale (4:5:6) usando ((3/2)^a)*((5/4)^b).
    a in [-a_max...a_max], b in [-b_max...b_max].
    """
    three_over_two: Fraction = Fraction(3, 2)
    five_over_four: Fraction = Fraction(5, 4)
    vals: list[Fraction | float] = []
    for a in range(-abs(a_max), abs(a_max) + 1):
        for b in range(-abs(b_max), abs(b_max) + 1):
            r = pow_fraction(three_over_two, a) * pow_fraction(five_over_four, b)
            vals.append(r)
    return normalize_ratios(vals, reduce_octave=reduce_octave)


def build_danielou_ratios(full_grid: bool = False, reduce_octave: bool = True) -> list[float]:
    """Genera rapporti del sistema Danielou.
    Formula: ((6/5)^a)*(3/2)^b*(2^c), con c per riduzione in ottava.
    - Se full_grid=True: produce 53 rapporti (dopo riduzione nell'ottava) come da richiesta.
    - Se full_grid=False: sottoinsieme: tonic (1/1), asse quinte (a=0, b=-5..5),
      tre terze minori armoniche successive ((6/5)^1...^3) e tre seste maggiori armoniche ((5/3)^1...^3).
    """
    six_over_five: Fraction = Fraction(6, 5)
    three_over_two: Fraction = Fraction(3, 2)
    vals: list[Fraction | float] = []
    if full_grid:
        # Griglia ampia e successivo pruning a 53 dopo riduzione
        for a in range(-3, 4):
            for b in range(-5, 6):
                r = pow_fraction(six_over_five, a) * pow_fraction(three_over_two, b)
                vals.append(r)
    else:
        vals.append(Fraction(1, 1))
        # Asse delle quinte (a=0)
        for b in range(-5, 6):
            vals.append(pow_fraction(three_over_two, b))
        # Tre terze minori armoniche successive
        for k in range(1, 4):
            vals.append(pow_fraction(six_over_five, k))
        # Tre seste maggiori armoniche successive
        five_over_three: Fraction = Fraction(5, 3)
        for k in range(1, 4):
            vals.append(pow_fraction(five_over_three, k))
    normalized = normalize_ratios(vals, reduce_octave=reduce_octave)
    if full_grid and reduce_octave and len(normalized) > 53:
        # Mantieni le 53 altezze più basse ordinate
        normalized = normalized[:53]
    return normalized


def danielou_from_exponents(a: int, b: int, c: int, reduce_octave: bool = True) -> list[float]:
    """Calcola un singolo rapporto del sistema Danielou dai tre esponenti (a,b,c).

    Formula: r = (6/5)^a * (3/2)^b * (2)^c
    - Se reduce_octave=True, riduce r nell'ottava [1,2).
    Restituisce una lista con un solo valore (float) per compatibilità con le pipeline di export.
    """
    six_over_five: Fraction = Fraction(6, 5)
    three_over_two: Fraction = Fraction(3, 2)
    two: Fraction = Fraction(2, 1)
    r: Fraction | float = (
        pow_fraction(six_over_five, int(a)) *
        pow_fraction(three_over_two, int(b)) *
        pow_fraction(two, int(c))
    )
    r = reduce_to_octave(r) if reduce_octave else r
    return [float(r) if isinstance(r, Fraction) else float(r)]


def reduce_to_octave(value: Fraction | float):
    """Riduce un rapporto nell'ambito di un'ottava [1, 2).

    - Se value è Fraction, mantiene aritmetica razionale.
    - Se value è float, opera in virgola mobile.
    """
    if isinstance(value, Fraction):
        two = Fraction(2, 1)
        while value >= two:
            value /= two
        while value < 1:
            value *= two
        return value
    else:
        # float
        while value >= 2.0:
            value /= 2.0
        while value < 1.0:
            value *= 2.0
        return value


def int_or_fraction(value):
    """Argparse type: interpreta una stringa come int oppure come Fraction.

    Esempi validi: "200", "3/2", "7/12". Solleva argparse.ArgumentTypeError
    in caso di valore non interpretabile.
    """
    try:
        return int(value)
    except ValueError:
        try:
            return Fraction(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{value}' non è un intero o una frazione valida.")


def ratio_et(index: int, cents: int | Fraction) -> float:
    """Calcola il rapporto della radice per un dato temperamento equabile.

    - index: indice della radice (es. 12 per 12-TET)
    - cents: ampiezza dell'intervallo in cents (di solito 1200) oppure già convertita

    Restituisce il rapporto r tale che r**index = exp(cents / (1200/log(2))).
    """
    decimal_number = math.exp((cents / ELLIS_CONVERSION_FACTOR))  # antilog
    ratio = decimal_number ** (1 / index)
    return ratio


def note_name_or_frequency(value):
    """Argparse type: prova a interpretare value come float (Hz), altrimenti stringa nota.

    Ritorna float se convertibile, altrimenti la stringa originale (es. "A4").
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return str(value)

def convert_note_name_to_midi(note_name: str):
    """Segnaposto per la conversione da nome di nota a Hz.

    In futuro: convert_note_name_to_hz(note_name: str, diapason_hz: float = 440.0) -> float
    """
    note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    note_name = note_name.strip().upper()
    note = note_name[0]
    if note not in note_map:
        raise ValueError(f"Nome nota non valido: {note_name}")
    alteration = 0
    index_octave_number = 1 # indice per il numero di ottava

    if len(note_name) > 1:
        if note_name[1] == '#':
            alteration = 1
            index_octave_number = 2
        elif note_name[1] == 'B':
            alteration = -1
            index_octave_number = 2

    try:
        octave = int(note_name[index_octave_number:]) # converte in int la sottostringa a partire da index_octave_number
    except (ValueError, IndexError):
        raise ValueError(f"Formato ottava non valido in: {note_name}")

    base_note_value = note_map[note]

    midi_value = (octave + 1) * 12 + base_note_value + alteration # +1 allinea MIDI e notazione scientifica (C4=MIDI 60)

    if not (0 <= midi_value <= 127):
        raise ValueError(f"Nota MIDI fuori range (0-127): {midi_value}")

    return midi_value

def convert_midi_to_hz(midi_value: int, diapason_hz: float = 440.0) -> float:
    # 1. calcola quanti semitoni midi_value è distante da A4 (valore 69)
    # 2. converte questo intervallo in semitoni in numero di ottave
    # 3. calcola il fattore per cui la frequenza deve essere moltiplicata
    # 4. moltiplica per il diapason specificato
    hz = diapason_hz * (2 ** ((float(midi_value) - 69) / 12))
    return hz

def file_exists(file_path: str) -> bool:
    """Verifica se il file esiste."""
    if os.path.exists(file_path):
        print(f"File esistente: {file_path}")
        return True
    else:
        print(f"File non esistente: {file_path}")
        return False

def parse_file(file_name: str) -> int:
    """Analizza il file alla ricerca di pattern 'f N' e ritorna il massimo N trovato.

    Se il file non esiste o non ci sono match, ritorna 0.
    """
    max_num: int | None = None
    try:
        with open(file_name, "r") as file:
            for line in file:
                for match in PATTERN.finditer(line):
                    num = int(match.group(1))
                    max_num = num if max_num is None else max(max_num, num)
    except FileNotFoundError:
        print(f"Errore: file non trovato: {file_name}")
        return 0
    return 0 if max_num is None else max_num


def write_frequency_table(output_base: str, rows: list[tuple[int, float]]) -> None:
    """[Deprecato] Scrive frequenze in '<output_base>.txt'. Mantenuto per compatibilità temporanea."""
    path = f"{output_base}.txt"
    try:
        mode = "a+" if file_exists(path) else "w"
        with open(path, mode) as file:
            for step_idx, freq in rows:
                file.write(f"{freq:.2f} Hz  Step {step_idx}\n")
        print(f"Tabella salvata in {path}")
    except Exception as e:
        print(f"Errore scrittura file: {e}")


def write_cpstun_table(output_base: str, ratios: list[float], basekey: int, basefrequency: float) -> tuple[int, bool]:
    """Crea o appende una tabella cpstun in un file Csound .csd.

    Formato GEN -2 atteso da cpstun:
    fN 0 size -2  numgrades interval basefreq basekey  r1 r2 r3 ...

    - numgrades: numero di gradi nell'intervallo (len(ratios))
    - interval: intervallo di ripetizione; 2.0 per ottava (se i rapporti sono in [1,2)),
      0.0 se non definibile (rapporti che superano l'ottava o nessuna ripetizione coerente)
    - basefreq: frequenza assoluta associata a basekey (basenote in Hz)
    - basekey: nota MIDI a cui si riferisce basefreq
    - r1..rn: rapporti unitari

    Ritorna una tupla (fnum, existed_before) dove:
    - fnum è il numero della tabella appena scritta;
    - existed_before indica se il file .csd esisteva già prima della scrittura.
    """
    csd_path = f"{output_base}.csd"
    skeleton = (
        "<CsoundSynthesizer>\n"
        "<CsOptions>\n\n</CsOptions>\n"
        "<CsInstruments>\n\n</CsInstruments>\n"
        "<CsScore>\n\n</CsScore>\n"
        "</CsoundSynthesizer>\n"
    )

    existed_before = file_exists(csd_path)
    if not existed_before:
        # crea scheletro .csd
        try:
            with open(csd_path, "w") as f:
                f.write(skeleton)
        except Exception as e:
            print(f"Errore creazione file CSD: {e}")
            return 0, existed_before

    # leggi contenuto corrente
    try:
        with open(csd_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Errore lettura CSD: {e}")
        return 0, existed_before

    # calcola prossimo numero di tabella
    f_max = parse_file(csd_path)
    fnum = (f_max or 0) + 1

    # determina header cpstun
    numgrades = int(len(ratios))
    # intervallo di ripetizione: 2.0 se tutti i rapporti sono nell'ottava [1,2), altrimenti 0.0
    try:
        rmin = min(float(r) for r in ratios) if ratios else 1.0
        rmax = max(float(r) for r in ratios) if ratios else 1.0
    except Exception:
        rmin, rmax = 1.0, 1.0
    interval = 2.0 if (rmin >= 1.0 and rmax < 2.0) else 0.0

    # compone la lista dati: header + ratios
    data_list: list[str] = []
    data_list.append(str(numgrades))                # numgrades (int)
    data_list.append(f"{float(interval):.10g}")    # interval
    data_list.append(f"{float(basefrequency):.10g}")  # basefreq
    data_list.append(str(int(basekey)))             # basekey
    data_list.extend(f"{float(r):.10f}" for r in ratios)

    # dimensione tabella = numero di dati forniti a GEN -2
    size = len(data_list)

    # Costruisce dinamicamente righe di commento allineate in modo che le etichette cadano sotto l'inizio dei token
    prefix = f"f {fnum} 0 {size} -2 "
    token_strs = list(data_list)
    # Calcola la colonna iniziale (0-based) di ciascun token nella riga f
    positions: list[int] = []
    col = len(prefix)
    for t in token_strs:
        positions.append(col)
        col += len(t) + 1  # token più spazio successivo

    def build_aligned_comment_line(label_map: list[tuple[int, str]]) -> str:
        # label_map: lista di (token_index, label_text) da posizionare su questa linea
        line = ";"  # il commento inizia con il punto e virgola
        base_offset = 1  # tiene conto del ';' che occupa la colonna 0
        for idx, text in label_map:
            target = base_offset + (positions[idx] if 0 <= idx < len(positions) else len(prefix))
            if target < len(line):
                # garantisce almeno uno spazio tra token ed etichetta
                target = len(line) + 1
            line += " " * (target - len(line)) + text
        return line + "\n"

    # Definisce quale etichetta finisce su quale linea
    line1 = build_aligned_comment_line([
        (0, "numgrades"),
        (2, "basefreq"),
        (4, "rapporti-di-intonazione .......")
    ])
    line2 = build_aligned_comment_line([
        (1, "interval"),
        (3, "basekey")
    ])
    header_comment = (
        line1 +
        line2 +
        f"; tabella cpstun generata automaticamente | basekey={basekey} basefrequency={basefrequency:.6f}Hz\n"
    )
    f_line = prefix + " ".join(data_list) + "\n"

    # inserisci prima di </CsScore>
    insert_marker = "</CsScore>"
    idx = content.rfind(insert_marker)
    if idx == -1:
        # struttura mancante: appende una sezione <CsScore>
        content = (
            content +
            "\n<CsScore>\n" + header_comment + f_line + "</CsScore>\n"
        )
    else:
        content = content[:idx] + header_comment + f_line + content[idx:]

    try:
        with open(csd_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Tabella cpstun (f {fnum}) salvata in {csd_path}")
    except Exception as e:
        print(f"Errore scrittura CSD: {e}")
        return (fnum, existed_before)

    return (fnum, existed_before)

def write_tun_file(output_base: str, ratios: list[float], basekey: int, basefrequency: float) -> None:
    """Esporta un file .tun (AnaMark TUN) con sezione [Exact Tuning] (Note 0..127 in Hz).

    - Mappa i passi generati su note MIDI consecutive a partire da basekey.
    - Le note non coperte dai passi vengono riempite con 12TET relativo a basekey.
    - basefrequency è la frequenza assoluta della basekey (basenote convertita in Hz).
    """
    tun_path = f"{output_base}.tun"
    lines: list[str] = []
    lines.append("[Tuning]")
    lines.append("FormatVersion=1")
    lines.append(f"Name=Generated by {__program_name__} {__version__}")
    lines.append("")
    lines.append("[Exact Tuning]")
    lines.append(f"; basekey={basekey} basefrequency={basefrequency:.6f}Hz")

    # Precomputa 12TET fallback relativo a basefrequency
    def tet_freq(offset_semitones: int) -> float:
        return basefrequency * (2.0 ** (offset_semitones / 12.0))

    for n in range(128):
        if 0 <= basekey <= 127 and (basekey <= n < basekey + len(ratios)):
            idx = n - basekey
            if 0 <= idx < len(ratios):
                freq = basefrequency * float(ratios[idx])
            else:
                freq = tet_freq(n - basekey)
        else:
            freq = tet_freq(n - basekey)
        lines.append(f"Note {n}={freq:.10f} Hz")

    try:
        with open(tun_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"File .tun salvato in {tun_path}")
    except Exception as e:
        print(f"Errore scrittura .tun: {e}")


def export_system_tables(output_base: str, ratios: list[float], basekey: int, basenote_hz: float) -> None:
    """Esporta tabelle del sistema generato (Hz / ratio / MIDI) in testo ed Excel.

    Crea:
    - {output_base}_system.txt (colonne allineate a larghezza fissa)
    - {output_base}_system.xlsx (se openpyxl disponibile)
    """
    # Testo - costruzione tabella a colonne allineate
    txt_path = f"{output_base}_system.txt"
    try:
        headers = ["Step", "MIDI", "Ratio", "Hz"]
        rows = []
        for i, r in enumerate(ratios):
            midi = basekey + i
            hz = basenote_hz * float(r)
            rows.append([
                str(i),
                str(midi),
                f"{float(r):.10f}",
                f"{hz:.6f}",
            ])
        # Calcola larghezze massime per colonna
        widths = [len(h) for h in headers]
        for row in rows:
            for c, val in enumerate(row):
                if len(val) > widths[c]:
                    widths[c] = len(val)
        # Funzione per formattare una riga con padding a destra
        def fmt(vals: list[str]) -> str:
            return "  ".join(val.ljust(widths[i]) for i, val in enumerate(vals))
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(fmt(headers) + "\n")
            for row in rows:
                f.write(fmt(row) + "\n")
        print(f"Esportato: {txt_path}")
    except Exception as e:
        print(f"Errore scrittura {txt_path}: {e}")

    # Excel
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        wb = Workbook()
        ws = wb.active
        ws.title = "System"
        headers = ["Step", "MIDI", "Ratio", "Hz"]
        ws.append(headers)
        header_fill = PatternFill(start_color="FFDDDDDD", end_color="FFDDDDDD", fill_type="solid")
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = header_fill
        for i, r in enumerate(ratios):
            midi = basekey + i
            hz = basenote_hz * float(r)
            ws.append([i, midi, float(r), hz])
        xlsx_path = f"{output_base}_system.xlsx"
        wb.save(xlsx_path)
        print(f"Esportato: {xlsx_path}")
    except ImportError:
        print("openpyxl non installato: export Excel saltato per _system.xlsx")
    except Exception as e:
        print(f"Errore export Excel _system.xlsx: {e}")


def export_comparison_tables(output_base: str, ratios: list[float], basekey: int, basenote_hz: float,
                             diapason_hz: float, compare_fund_hz: float | None = None, tet_align: str = "same") -> None:
    """Esporta tabelle di confronto con 12TET e con la serie armonica.

    Crea:
    - {output_base}_compare.txt
    - {output_base}_compare.xlsx (se openpyxl disponibile)
    Colonne TXT: Step, MIDI, Ratio, Custom_Hz, Harmonic_Hz, DeltaHz_Harm, TET_Hz, DeltaHz_TET
    In Excel abbiniamo valori vicini affiancandoli (Custom accanto a Harmonic) e li coloriamo
    con colori diversi: Custom in rosso, Harmonic in verde, TET in blu. Se |Delta| < 17 Hz
    tra Custom e Harmonic, evidenziamo entrambi in grassetto.

    Parametri aggiuntivi:
    - compare_fund_hz: fondamentale per la serie armonica e per l'ancoraggio del 12TET.
      Se None, si usa basenote_hz.
    - tet_align: "same" (il 12TET parte esattamente da compare_fund_hz) oppure "nearest"
      (per ogni Custom si prende la nota 12TET più vicina nel reticolo ancorato a compare_fund_hz).
    """
    proximity_thr = 17.0  # Hz per considerare "vicini"

    base_cmp = compare_fund_hz if compare_fund_hz is not None else basenote_hz

    def tet_from_base(step_i: int, custom_val: float | None = None) -> float:
        if tet_align == "nearest" and custom_val is not None and custom_val > 0 and base_cmp > 0:
            # trova il grado 12TET più vicino a custom_val nel reticolo ancorato a base_cmp
            n = round(12.0 * math.log2(custom_val / base_cmp))
            return base_cmp * (2.0 ** (n / 12.0))
        # default: stesso indice i dalla fondamentale
        return base_cmp * (2.0 ** (step_i / 12.0))

    # Testo (mettiamo Custom e Harmonic affiancati) con colonne allineate a larghezza fissa
    txt_path = f"{output_base}_compare.txt"
    try:
        headers = [
            "Step", "MIDI", "Ratio",
            "Custom_Hz", "Harmonic_Hz", "DeltaHz_Harm",
            "TET_Hz", "DeltaHz_TET",
        ]
        rows: list[list[str]] = []
        for i, r in enumerate(ratios):
            midi = basekey + i
            custom_hz = basenote_hz * float(r)
            harm_hz = base_cmp * (i + 1)
            tet_hz = tet_from_base(i, custom_hz)
            d_tet = custom_hz - tet_hz
            d_har = custom_hz - harm_hz
            approx = "≈" if abs(d_har) < proximity_thr else ""
            rows.append([
                str(i),
                str(midi),
                f"{float(r):.10f}",
                f"{custom_hz:.6f}{approx}",
                f"{harm_hz:.6f}{approx}",
                f"{d_har:.6f}",
                f"{tet_hz:.6f}",
                f"{d_tet:.6f}",
            ])
        # Calcola larghezze massime per colonna
        widths = [len(h) for h in headers]
        for row in rows:
            for c, val in enumerate(row):
                if len(val) > widths[c]:
                    widths[c] = len(val)
        def fmt(vals: list[str]) -> str:
            return "  ".join(val.ljust(widths[i]) for i, val in enumerate(vals))
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(fmt(headers) + "\n")
            for row in rows:
                f.write(fmt(row) + "\n")
        print(f"Esportato: {txt_path}")
    except Exception as e:
        print(f"Errore scrittura {txt_path}: {e}")

    # Excel
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        wb = Workbook()
        ws = wb.active
        ws.title = "Compare"
        headers = [
            "Step", "MIDI", "Ratio",
            "Custom_Hz", "Harmonic_Hz", "|DeltaHz_Harm|",
            "TET_Hz", "|DeltaHz_TET|",
        ]
        ws.append(headers)
        header_fill = PatternFill(start_color="FFCCE5FF", end_color="FFCCE5FF", fill_type="solid")
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = header_fill

        # Riempimenti per le serie
        fill_custom = PatternFill(start_color="FFFFCCCC", end_color="FFFFCCCC", fill_type="solid")  # rosso chiaro
        fill_harm = PatternFill(start_color="FFCCFFCC", end_color="FFCCFFCC", fill_type="solid")    # verde chiaro
        fill_tet = PatternFill(start_color="FFCCE5FF", end_color="FFCCE5FF", fill_type="solid")      # blu chiaro

        for i, r in enumerate(ratios):
            midi = basekey + i
            custom_hz = basenote_hz * float(r)
            harm_hz = base_cmp * (i + 1)
            tet_hz = tet_from_base(i, custom_hz)
            d_tet = custom_hz - tet_hz
            d_har = custom_hz - harm_hz
            ws.append([i, midi, float(r), custom_hz, harm_hz, abs(d_har), tet_hz, abs(d_tet)])
            row = ws.max_row
            # Applica colorazione per serie
            ws.cell(row=row, column=4).fill = fill_custom
            ws.cell(row=row, column=5).fill = fill_harm
            ws.cell(row=row, column=7).fill = fill_tet
            # Evidenziazione di prossimità tra Custom e Harmonic
            is_close = abs(d_har) < proximity_thr
            if is_close:
                ws.cell(row=row, column=4).font = Font(bold=True)
                ws.cell(row=row, column=5).font = Font(bold=True)
        xlsx_path = f"{output_base}_compare.xlsx"
        wb.save(xlsx_path)
        print(f"Esportato: {xlsx_path}")
    except ImportError:
        print("openpyxl non installato: export Excel saltato per _compare.xlsx")
    except Exception as e:
        print(f"Errore export Excel _compare.xlsx: {e}")


def main():
    """Punto di ingresso CLI.

    - Mostra l'help di argparse quando non vengono passati argomenti.
    - Imposta e valida gli argomenti della riga di comando.
    - Esegue il calcolo del rapporto della radice per il temperamento richiesto.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Assistente software per i sistemi di intonazione musicali. "
            "Generatore di tabelle/rapporti per cpstun in Csound e tabelle di comparazione con 12TET. "
            f"Versione {__version__}"
        ),
        epilog="Autore: LUCA BIMBI, Agosto 2025"
    )

    # Versione del programma
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}",
                        help="Visualizza la versione del programma")

    # Diapason di riferimento in Hz (stringa per lasciare libertà input; conversione demandata altrove)
    parser.add_argument("--diapason", type=float, default=440.0,
                        help="Diapason di riferimento in Hz (default: 440)")

    # Nota base per tabella cpstun (MIDI key), default 60 (C4)
    parser.add_argument(
        "--basekey", default=60, type=int,
        help="Nota base (MIDI key) per tabella cpstun (default: 60)"
    )

    # Nota/frequenza di riferimento
    parser.add_argument(
        "--basenote", default="440", type=note_name_or_frequency, required=True,
        help="Nota di riferimento (es. 'A4', 'F#2', 'Ab3') o frequenza in Hz"
    )

    # Temperamento equabile: indice della radice e ampiezza in cents (o frazione convertibile)
    parser.add_argument(
        "-et", nargs=2, default=(12, 200), type=int_or_fraction,
        help=(
            "Temperamento equabile definibile dall'utente. "
            "Richiede: indice della radice e valore dell'intervallo in cents (o frazione)."
        ),
    )

    # Sistema geometrico basato su un generatore (es. 3/2) e numero di passi
    parser.add_argument(
        "--geometric", nargs=2, metavar=("GEN", "STEPS"),
        help=(
            "Sistema geometrico su generatore (es. 3/2) e passi. "
            "Esempio: --geometric 3/2 12"
        ),
    )
    # Sistema naturale (4:5:6)
    parser.add_argument(
        "--natural", nargs=2, type=int, metavar=("A_MAX", "B_MAX"),
        help=(
            "Sistema naturale 4:5:6 con ((3/2)^a)*((5/4)^b), a∈[-A_MAX..A_MAX], b∈[-B_MAX..B_MAX]"
        ),
    )
    # Sistema Danielou
    parser.add_argument(
        "--danielou", action="store_true",
        help="Genera il sistema Danielou (sottoinsieme predefinito)"
    )
    parser.add_argument(
        "--danielou-all", action="store_true",
        help="Usa la griglia completa Danielou (a=-3..3, b=-5..5) per ottenere fino a 53 rapporti"
    )
    # Esponenti Danielou (a,b,c)
    parser.add_argument(
        "--danielou-a", type=int, default=None,
        help="Esponente a per (6/5)^a nel sistema Danielou"
    )
    parser.add_argument(
        "--danielou-b", type=int, default=None,
        help="Esponente b per (3/2)^b nel sistema Danielou"
    )
    parser.add_argument(
        "--danielou-c", type=int, default=None,
        help="Esponente c per (2)^c nel sistema Danielou"
    )
    parser.add_argument(
        "--no-reduce", action="store_true",
        help="Non ridurre i rapporti all'interno dell'ottava (default: riduci)",
    )
    parser.add_argument(
        "--export-tun", action="store_true",
        help="Esporta anche un file .tun (AnaMark TUN) con [Exact Tuning] su 128 note",
    )

    # Opzioni per il confronto (serie armonica e 12TET)
    parser.add_argument(
        "--compare-fund", type=note_name_or_frequency, default=None,
        help="Fondamentale per il confronto (nota es. 'A4' o frequenza in Hz). Default: basenote"
    )
    parser.add_argument(
        "--compare-tet-align", choices=["same", "nearest"], default="same",
        help="Allineamento 12TET nel confronto: 'same' dalla fondamentale, 'nearest' nota 12TET più vicina alla Custom"
    )

    # File di output (non ancora utilizzato in questa versione)
    parser.add_argument("output_file", help="File di output con la tabella di accordatura")

    # Se non sono stati passati argomenti, mostra l'help e termina
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    # Validazione basenote
    if isinstance(args.basenote, (int, float)) and args.basenote < 0:
        print("Nota di riferimento non valida.")
        return

    # Determina la frequenza di base in Hz: se float, è già Hz; altrimenti sarebbe da convertire
    if isinstance(args.basenote, float):
        basenote = args.basenote
    else:
        # conversione del nome nota, utilizzando il diapason
        basenote_midi = convert_note_name_to_midi(args.basenote)
        basenote = convert_midi_to_hz(basenote_midi, args.diapason)

    # Determina la fondamentale per il confronto (serie armonica e ancoraggio 12TET)
    if args.compare_fund is None:
        compare_fund_hz = basenote
    else:
        if isinstance(args.compare_fund, float):
            compare_fund_hz = args.compare_fund
        else:
            # è un nome di nota: convertilo con il diapason corrente
            cf_midi = convert_note_name_to_midi(args.compare_fund)
            compare_fund_hz = convert_midi_to_hz(cf_midi, args.diapason)

    # Sistema naturale (4:5:6): priorità alta rispetto a geometric/ET
    if args.natural:
        try:
            a_max = int(args.natural[0])
            b_max = int(args.natural[1])
        except (TypeError, ValueError):
            print("Valori non validi per --natural (attesi interi A_MAX B_MAX).")
            return
        if a_max < 0 or b_max < 0:
            print("A_MAX e B_MAX devono essere >= 0 per --natural.")
            return
        ratios = build_natural_ratios(a_max, b_max, reduce_octave=(not args.no_reduce))
        for i, r in enumerate(ratios):
            freq = basenote * float(r)
            print(f"{freq:.2f} Hz  Step {i+1}")
        fnum, existed = write_cpstun_table(args.output_file, ratios, args.basekey, basenote)
        export_base = args.output_file if not existed else f"{args.output_file}_{fnum}"
        export_system_tables(export_base, ratios, args.basekey, basenote)
        try:
            diapason_hz = float(args.diapason)
        except TypeError:
            diapason_hz = 440.0
        export_comparison_tables(export_base, ratios, args.basekey, basenote, diapason_hz,
                                 compare_fund_hz=compare_fund_hz, tet_align=args.compare_tet_align)
        if args.export_tun:
            write_tun_file(export_base, ratios, args.basekey, basenote)
        return

    # Sistema Danielou tramite esponenti (a,b,c): ha priorità se specificati
    if (args.danielou_a is not None) or (args.danielou_b is not None) or (args.danielou_c is not None):
        if (args.danielou_a is None) or (args.danielou_b is None) or (args.danielou_c is None):
            print("Per usare gli esponenti Danielou specifica tutti e tre: --danielou-a --danielou-b --danielou-c")
            return
        try:
            a = int(args.danielou_a)
            b = int(args.danielou_b)
            c = int(args.danielou_c)
        except (TypeError, ValueError):
            print("Esponenti non validi per Danielou (devono essere interi).")
            return
        ratios = danielou_from_exponents(a, b, c, reduce_octave=(not args.no_reduce))
        for i, r in enumerate(ratios):
            freq = basenote * float(r)
            print(f"{freq:.2f} Hz  Step {i+1}")
        fnum, existed = write_cpstun_table(args.output_file, ratios, args.basekey, basenote)
        export_base = args.output_file if (not existed or fnum <= 1) else f"{args.output_file}_{fnum}"
        export_system_tables(export_base, ratios, args.basekey, basenote)
        try:
            diapason_hz = float(args.diapason)
        except TypeError:
            diapason_hz = 440.0
        export_comparison_tables(export_base, ratios, args.basekey, basenote, diapason_hz,
                                 compare_fund_hz=compare_fund_hz, tet_align=args.compare_tet_align)
        if args.export_tun:
            write_tun_file(export_base, ratios, args.basekey, basenote)
        return

    # Sistema Danielou: controlla sia --danielou che --danielou-all
    if args.danielou or args.danielou_all:
        full = bool(args.danielou_all)
        ratios = build_danielou_ratios(full_grid=full, reduce_octave=(not args.no_reduce))
        for i, r in enumerate(ratios):
            freq = basenote * float(r)
            print(f"{freq:.2f} Hz  Step {i+1}")
        fnum, existed = write_cpstun_table(args.output_file, ratios, args.basekey, basenote)
        export_base = args.output_file if (not existed or fnum <= 1) else f"{args.output_file}_{fnum}"
        export_system_tables(export_base, ratios, args.basekey, basenote)
        try:
            diapason_hz = float(args.diapason)
        except TypeError:
            diapason_hz = 440.0
        export_comparison_tables(export_base, ratios, args.basekey, basenote, diapason_hz,
                                 compare_fund_hz=compare_fund_hz, tet_align=args.compare_tet_align)
        if args.export_tun:
            write_tun_file(export_base, ratios, args.basekey, basenote)
        return

    # Sistema geometrico: se specificato, priorità rispetto a -et
    if args.geometric:
        gen_str, steps_str = args.geometric
        try:
            steps = int(steps_str)
            if steps <= 0:
                print("Numero di passi deve essere > 0 per --geometric.")
                return
        except ValueError:
            print("Numero di passi non valido per --geometric.")
            return
        # parsing generatore
        try:
            gen_val = int_or_fraction(gen_str)
        except argparse.ArgumentTypeError:
            try:
                gen_val = float(gen_str)
            except ValueError:
                print("Generatore non valido per --geometric.")
                return
        # normalizza tipo
        if isinstance(gen_val, int):
            gen_ratio = Fraction(gen_val, 1)
        elif isinstance(gen_val, Fraction):
            gen_ratio = gen_val
        else:
            gen_ratio = float(gen_val)

        # validazione generatore > 0
        try:
            gen_numeric = float(gen_ratio) if not isinstance(gen_ratio, Fraction) else float(gen_ratio)
        except TypeError:
            print("Generatore non numerico per --geometric.")
            return
        if gen_numeric <= 0:
            print("Il generatore deve essere > 0 per --geometric.")
            return

        ratios: list[float] = []
        for i in range(steps):
            # potenza del generatore
            if isinstance(gen_ratio, Fraction):
                r = gen_ratio ** i
            else:
                r = (float(gen_ratio)) ** i
            # riduzione all'ottava di default
            r_reduced = reduce_to_octave(r) if not args.no_reduce else r
            r_value = float(r_reduced) if isinstance(r_reduced, Fraction) else float(r_reduced)
            freq = basenote * r_value
            ratios.append(r_value)
            print(f"{freq:.2f} Hz  Step {i+1}")
        fnum, existed = write_cpstun_table(args.output_file, ratios, args.basekey, basenote)
        export_base = args.output_file if not existed else f"{args.output_file}_{fnum}"
        export_system_tables(export_base, ratios, args.basekey, basenote)
        try:
            diapason_hz = float(args.diapason)
        except TypeError:
            diapason_hz = 440.0
        export_comparison_tables(export_base, ratios, args.basekey, basenote, diapason_hz,
                                 compare_fund_hz=compare_fund_hz, tet_align=args.compare_tet_align)
        if args.export_tun:
            write_tun_file(export_base, ratios, args.basekey, basenote)
        return

    # Validazione presenza -et
    if not args.et:
        print("Temperamento equabile non specificato. Usa -et indice cents")
        return

    index, cents = args.et

    # Controlli di base
    if index <= 0 or (isinstance(cents, (int, float)) and cents <= 0):
        print("Indice della radice o valore di cents non valido.")
        return

    # Se l'utente ha passato una frazione, convertirla in cents
    if is_fraction_type(args.et[1]):
        print("rilevato numero razionale espresso in frazione, conversione in cents...")
        cents = fraction_to_cents(args.et[1])
        print(f"Conversione di {Fraction(args.et[1])} in cents: {cents}")

    print(f"index: {index}, cents: {cents}")

    try:
        ratio = ratio_et(index, cents)
        print(f"Ratio: {ratio}")
    except ZeroDivisionError:
        print("errore di divisione per zero")
        return

    ratios: list[float] = []
    for i in range(index):
        r_value = float(ratio ** i)
        freq = basenote * r_value
        print(f"{freq:.2f} Hz  Step {i+1}")
        ratios.append(r_value)
    fnum, existed = write_cpstun_table(args.output_file, ratios, args.basekey, basenote)
    export_base = args.output_file if not existed else f"{args.output_file}_{fnum}"
    export_system_tables(export_base, ratios, args.basekey, basenote)
    try:
        diapason_hz = float(args.diapason)
    except TypeError:
        diapason_hz = 440.0
    export_comparison_tables(export_base, ratios, args.basekey, basenote, diapason_hz,
                             compare_fund_hz=compare_fund_hz, tet_align=args.compare_tet_align)
    if args.export_tun:
        write_tun_file(export_base, ratios, args.basekey, basenote)
if __name__ == "__main__":
    main()