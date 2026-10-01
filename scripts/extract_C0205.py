#!/usr/bin/env python3
import json,sqlite3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ids=["C0204","C0299"]
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
out={}
for cid in ids:
    r=con.execute("select titulo,letra from cancion where cancion_id=?",(cid,)).fetchone()
    if not r: raise SystemExit(cid)
    out[cid]={"titulo":r[0],"letra":r[1] or ""}
con.close()
(R/"scripts"/"review_0204_0299_lyrics.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
