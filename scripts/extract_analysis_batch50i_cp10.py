#!/usr/bin/env python3
import sqlite3,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ids=["C0260","C0262","C0264","C0265","C0266","C0267","C0268"]
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
out={}
for cid in ids:
    row=con.execute("select titulo,letra from cancion where cancion_id=?",(cid,)).fetchone()
    if not row: raise SystemExit(cid)
    out[cid]={"titulo":row[0],"letra":row[1]}
con.close()
(R/"scripts"/"analysis_batch50i_cp10_lyrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(out))
