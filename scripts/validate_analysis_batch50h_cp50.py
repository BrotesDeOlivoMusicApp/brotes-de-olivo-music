#!/usr/bin/env python3
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
L=json.loads((R/"scripts"/"analysis_batch50h_lyrics.json").read_text(encoding="utf-8"))
C=json.loads((R/"scripts"/"analysis_batch50h_cp50_candidates.json").read_text(encoding="utf-8"))
expected={"C0250","C0252","C0254","C0256","C0258"}
if set(C)!=expected: raise SystemExit(f"IDs inesperados {sorted(C)}")
bad=[]
for cid in sorted(expected):
    plain=re.sub(r"\[[^\]\n]+\]","",C[cid])
    if plain!=L[cid]["letra"]: bad.append((cid,"texto"))
    if C[cid].count("[")!=C[cid].count("]"): bad.append((cid,"corchetes"))
    if "[" not in C[cid]: bad.append((cid,"sin acordes"))
if bad: raise SystemExit(repr(bad))
print("OK 5/5 checkpoint 50")
