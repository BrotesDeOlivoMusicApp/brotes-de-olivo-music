#!/usr/bin/env python3
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch30f_lyrics.json").read_text(encoding="utf-8"))
C=json.loads((R/"scripts"/"analysis_batch30f_candidates.json").read_text(encoding="utf-8"))
expected={"C0209","C0210","C0211","C0212","C0213","C0214","C0215","C0216","C0218","C0219"}
if set(C)!=expected: raise SystemExit(f"IDs inesperados {sorted(C)}")
bad=[]
for cid in sorted(expected):
    plain=re.sub(r"\[[^\]\n]+\]","",C[cid])
    if plain!=L[cid]["letra"]: bad.append((cid,"texto"))
    if C[cid].count("[")!=C[cid].count("]"): bad.append((cid,"corchetes"))
    if "[" not in C[cid]: bad.append((cid,"sin acordes"))
if bad: raise SystemExit(repr(bad))
print("OK 10/10 candidatos: texto V11 exacto, corchetes balanceados y acordes presentes")
