#!/usr/bin/env python3
import sqlite3,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ids=[f"C{n:04d}" for n in range(171,181)]
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
out={}
for cid in ids:
    row=con.execute("select titulo,letra from cancion where cancion_id=?",(cid,)).fetchone()
    if not row: raise SystemExit(f"Falta {cid}")
    out[cid]={"titulo":row[0],"letra":row[1]}
con.close()
(R/"scripts"/"analysis_batch4_lyrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
