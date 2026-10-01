#!/usr/bin/env python3
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch20c_lyrics.json").read_text(encoding="utf-8"))
C=json.loads((R/"scripts"/"analysis_batch20c_candidates.json").read_text(encoding="utf-8"))
expected={"C0067","C0068","C0069","C0070","C0071","C0072","C0074","C0075","C0076","C0077","C0078","C0079","C0080","C0081","C0082","C0083","C0084"}
if set(C)!=expected: raise SystemExit(f"IDs inesperados {sorted(C)}")
bad=[]
for cid in sorted(expected):
    plain=re.sub(r"\[[^\]\n]+\]","",C[cid])
    if plain!=L[cid]["letra"]: bad.append((cid,"texto"))
    if C[cid].count("[")!=C[cid].count("]"): bad.append((cid,"corchetes"))
    if "[" not in C[cid]: bad.append((cid,"sin acordes"))
if bad: raise SystemExit(repr(bad))
print("OK 17/17 candidatos: texto V11 exacto y sintaxis balanceada")
