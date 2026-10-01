#!/usr/bin/env python3
import json,sqlite3,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"
cand=json.loads((R/"scripts"/"import_prepared_35.json").read_text(encoding="utf-8"))
if len(cand)!=35: raise SystemExit(f"Esperaba 35 y hay {len(cand)}")
con=sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=126: raise SystemExit(f"Esperaba 126 y hay {before}")
    for cid,txt in sorted(cand.items()):
        row=con.execute("select letra,acordes from cancion where cancion_id=?",(cid,)).fetchone()
        if not row: raise SystemExit(f"Falta {cid}")
        if (row[1] or "").strip(): raise SystemExit(f"{cid} ya tiene acordes")
        plain=re.sub(r"\[[^\]\n]+\]","",txt)
        if plain!=(row[0] or ""): raise SystemExit(f"{cid}: letra no coincide")
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    con.commit()
    if con.execute("pragma integrity_check").fetchone()[0]!="ok": raise SystemExit("integrity_check")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk: raise SystemExit(f"foreign_key_check {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=161: raise SystemExit(f"Esperaba 161 y hay {after}")
finally: con.close()
info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.10.01.3": raise SystemExit(f"Versión inesperada {info.get('dataVersion')}")
sha=hashlib.sha256(DB.read_bytes()).hexdigest()
info["dataVersion"]="2026.10.01.4"
info["sha256"]=sha
info["date"]="2026-10-01"
info["notes"]="Séptimo lote de acordes: 35 canciones preparadas importadas. Total acumulado: 161 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK 35 importadas; total 161; dataVersion",info["dataVersion"],"sha",sha)
