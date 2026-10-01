#!/usr/bin/env python3
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
lyrics=json.loads((R/"scripts"/"aliento_vida_lyrics.json").read_text(encoding="utf-8"))
cand=json.loads((R/"scripts"/"aliento_candidates_10.json").read_text(encoding="utf-8"))
expected=[f"C{n:04d}" for n in range(118,128)]
if sorted(cand)!=expected:
    raise SystemExit(f"IDs inesperados: {sorted(cand)}")
bad=[]
for cid in expected:
    c=cand[cid]
    plain=re.sub(r"\[[^\]\n]+\]","",c)
    if plain!=lyrics[cid]["letra"]:
        bad.append((cid,"texto"))
    if c.count("[")!=c.count("]"):
        bad.append((cid,"corchetes"))
    if "[" not in c:
        bad.append((cid,"sin acordes"))
if bad:
    raise SystemExit("Fallos: "+repr(bad))
print("OK: 10/10 candidatos; texto subyacente exacto a V11 y sintaxis balanceada")
