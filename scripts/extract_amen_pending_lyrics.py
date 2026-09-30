#!/usr/bin/env python3
import json,sqlite3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
OUT=R/"scripts"/"amen_pending_lyrics.json"
ids="C0003 C0004 C0005 C0007 C0008 C0012 C0013".split()
con=sqlite3.connect(DB)
out={}
for cid in ids:
    row=con.execute("select titulo,letra from cancion where cancion_id=?",(cid,)).fetchone()
    if row is None: raise SystemExit(f"Falta {cid}")
    out[cid]={"titulo":row[0],"letra":row[1] or ""}
con.close()
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK",len(out))
