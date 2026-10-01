#!/usr/bin/env python3
import json,re,sqlite3,difflib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
cand=json.loads((R/"scripts"/"review_candidates_4.json").read_text(encoding="utf-8"))
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
ok=[]; bad=[]
for cid,txt in cand.items():
    row=con.execute("select letra from cancion where cancion_id=?",(cid,)).fetchone()
    if not row:
        bad.append((cid,"ID inexistente")); continue
    letra=(row[0] or "").replace("\r\n","\n").rstrip()
    txt=txt.replace("\r\n","\n").rstrip()
    if txt.count("[")!=txt.count("]"):
        bad.append((cid,"corchetes desbalanceados")); continue
    plain=re.sub(r"\[[^\]\r\n]+\]","",txt)
    if plain!=letra:
        sm=difflib.SequenceMatcher(a=letra,b=plain)
        ops=[]
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!="equal":
                ops.append(f"{tag} DB[{i1}:{i2}]={letra[i1:i2]!r} CAND[{j1}:{j2}]={plain[j1:j2]!r}")
        bad.append((cid," | ".join(ops[:12]))); continue
    ok.append(cid)
con.close()
print("VALIDAS",len(ok)," ".join(ok))
if bad:
    print("FALLOS",len(bad))
    for x in bad: print(*x)
    raise SystemExit(1)
print("OK 4/4")
