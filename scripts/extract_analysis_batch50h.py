#!/usr/bin/env python3
import sqlite3,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ids=["C0230","C0231","C0232","C0233","C0234","C0235","C0238","C0240","C0242","C0244","C0246","C0248","C0250","C0252","C0254","C0256","C0258"]
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
out={}
for cid in ids:
    row=con.execute("select titulo,letra from cancion where cancion_id=?",(cid,)).fetchone()
    if not row: raise SystemExit(cid)
    out[cid]={"titulo":row[0],"letra":row[1]}
con.close()
(R/"scripts"/"analysis_batch50h_lyrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
