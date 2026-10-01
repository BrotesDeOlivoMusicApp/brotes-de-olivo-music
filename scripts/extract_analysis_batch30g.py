#!/usr/bin/env python3
import sqlite3,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ids=["C0220","C0221","C0222","C0224","C0225","C0226","C0227","C0228","C0229"]
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
out={}
for cid in ids:
    row=con.execute("select titulo,letra from cancion where cancion_id=?",(cid,)).fetchone()
    if not row: raise SystemExit(cid)
    out[cid]={"titulo":row[0],"letra":row[1]}
con.close()
(R/"scripts"/"analysis_batch30g_lyrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
