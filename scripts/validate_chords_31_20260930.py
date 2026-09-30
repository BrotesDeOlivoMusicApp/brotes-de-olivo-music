#!/usr/bin/env python3
# Revalidación final tras ajuste de C0295
import json, re, sqlite3, difflib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"data"/"brotes_publica.sqlite"
batch_files=[ROOT/"scripts"/f"chords_review_batch_{i}.json" for i in range(1,5)]

def strip_chords(s):
    return re.sub(r"\[[^\]\r\n]+\]", "", s).replace("\r\n","\n").rstrip()

def syntax_ok(s):
    tokens=re.findall(r"\[([^\]\r\n]+)\]", s)
    return bool(tokens) and s.count("[")==s.count("]")==len(tokens)

candidates={}
for p in batch_files:
    candidates.update(json.loads(p.read_text(encoding="utf-8")))

con=sqlite3.connect(DB)
bad=[]; ok=[]
for cid,cand in sorted(candidates.items()):
    row=con.execute("select letra from cancion where cancion_id=?",(cid,)).fetchone()
    if row is None:
        bad.append((cid,"ID no existe")); continue
    letra=(row[0] or "").replace("\r\n","\n").rstrip()
    cand=cand.replace("\r\n","\n").rstrip()
    if not syntax_ok(cand):
        bad.append((cid,"sintaxis de corchetes/acordes inválida")); continue
    plain=strip_chords(cand)
    if plain != letra:
        n=min(len(plain),len(letra))
        pos=next((i for i in range(n) if plain[i]!=letra[i]),n)
        sm=difflib.SequenceMatcher(a=letra,b=plain)
        ops=[]
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!="equal":
                ops.append(f"{tag} DB[{i1}:{i2}]={letra[i1:i2]!r} CAND[{j1}:{j2}]={plain[j1:j2]!r}")
        bad.append((cid,f"texto difiere; len={len(plain)}/{len(letra)}; " + " | ".join(ops[:8]))); continue
    ok.append(cid)
con.close()
print("VALIDAS",len(ok)," ".join(ok))
if bad:
    print("FALLOS",len(bad))
    for cid,why in bad: print(cid,why)
    raise SystemExit(1)
if len(ok)!=31:
    raise SystemExit(f"Esperaba 31 candidatas y validé {len(ok)}")
print("OK 31/31")
