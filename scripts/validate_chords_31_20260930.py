#!/usr/bin/env python3
import re, sqlite3, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/"data"/"brotes_publica.sqlite"
IDS="""C0165 C0166 C0168 C0169 C0197 C0199 C0200 C0201 C0202 C0203 C0206 C0207 C0208 C0293 C0294 C0295 C0296 C0297 C0298 C0300 C0301 C0302 C0303 C0304 C0305 C0306 C0307 C0308 C0310 C0311 C0312""".split()
BASE="https://raw.githubusercontent.com/BrotesDeOlivoMusicApp/brotes-de-olivo/main/docs/acordes/trabajo/canciones/{}.txt"

def strip_chords(s):
    s=re.sub(r"\[[^\]\r\n]+\]", "", s)
    return s.replace("\r\n","\n").rstrip()

def syntax_ok(s):
    # all [ must belong to a closed non-empty token, and no stray ]
    tokens=re.findall(r"\[([^\]\r\n]+)\]", s)
    return bool(tokens) and s.count("[")==s.count("]")==len(tokens)

con=sqlite3.connect(DB)
bad=[]
ok=[]
for cid in IDS:
    row=con.execute("select letra from cancion where cancion_id=?",(cid,)).fetchone()
    if row is None:
        bad.append((cid,"ID no existe"))
        continue
    letra=(row[0] or "").replace("\r\n","\n").rstrip()
    try:
        with urllib.request.urlopen(BASE.format(cid), timeout=20) as r:
            cand=r.read().decode("utf-8").replace("\r\n","\n").rstrip()
    except Exception as e:
        bad.append((cid,f"no se pudo descargar candidato: {e}"))
        continue
    if not syntax_ok(cand):
        bad.append((cid,"sintaxis de corchetes/acordes inválida"))
        continue
    stripped=strip_chords(cand)
    if stripped != letra:
        # report first differing offset without dumping copyrighted text
        n=min(len(stripped),len(letra))
        pos=next((i for i in range(n) if stripped[i]!=letra[i]), n)
        bad.append((cid,f"texto difiere de letra V11 en offset {pos}; len candidato={len(stripped)}, len letra={len(letra)}"))
        continue
    ok.append(cid)
con.close()

print("APROBADAS_TECNICAMENTE", len(ok), " ".join(ok))
if bad:
    print("FALLOS", len(bad))
    for cid,why in bad: print(cid, why)
    raise SystemExit(1)
print("OK: 31/31 coinciden exactamente con cancion.letra V11 y tienen sintaxis de acordes balanceada.")
