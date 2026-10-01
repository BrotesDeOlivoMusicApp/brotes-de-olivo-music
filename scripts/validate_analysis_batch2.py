#!/usr/bin/env python3
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L={}
L.update(json.loads((R/"scripts"/"aliento_vida_lyrics.json").read_text(encoding="utf-8")))
L.update(json.loads((R/"scripts"/"analysis_batch2_lyrics.json").read_text(encoding="utf-8")))
C=json.loads((R/"scripts"/"analysis_batch2_candidates.json").read_text(encoding="utf-8"))
expected=["C0128","C0129","C0132","C0147","C0148","C0149","C0150"]
if sorted(C)!=sorted(expected): raise SystemExit(f"IDs inesperados {sorted(C)}")
bad=[]
for cid in expected:
    plain=re.sub(r"\[[^\]\n]+\]","",C[cid])
    if plain!=L[cid]["letra"]: bad.append((cid,"texto"))
    if C[cid].count("[")!=C[cid].count("]"): bad.append((cid,"corchetes"))
    if "[" not in C[cid]: bad.append((cid,"sin acordes"))
if bad: raise SystemExit(repr(bad))
print("OK 7/7 candidatos: texto V11 exacto y sintaxis balanceada")
