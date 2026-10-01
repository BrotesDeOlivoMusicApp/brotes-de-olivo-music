#!/usr/bin/env python3
import json,sqlite3,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"
cand=json.loads((R/"scripts"/"import_prepared_4.json").read_text(encoding="utf-8"))
if set(cand)!={"C0003","C0004","C0204","C0299"}: raise SystemExit("IDs inesperados")
con=sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=83: raise SystemExit(f"Esperaba 83 y hay {before}")
    for cid,txt in cand.items():
        row=con.execute("select acordes from cancion where cancion_id=?",(cid,)).fetchone()
        if not row: raise SystemExit(f"Falta {cid}")
        if (row[0] or "").strip(): raise SystemExit(f"{cid} ya tiene acordes")
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    con.commit()
    if con.execute("pragma integrity_check").fetchone()[0]!="ok": raise SystemExit("integrity_check falló")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk: raise SystemExit(f"foreign_key_check: {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=87: raise SystemExit(f"Esperaba 87 y hay {after}")
finally: con.close()
info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.10.01.1": raise SystemExit(f"Versión inesperada {info.get('dataVersion')}")
sha=hashlib.sha256(DB.read_bytes()).hexdigest()
info["dataVersion"]="2026.10.01.2"
info["sha256"]=sha
info["date"]="2026-10-01"
info["notes"]="Quinto lote de acordes: 4 casos revisados importados. Total acumulado: 87 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK 4 importadas; total 87; dataVersion",info["dataVersion"],"sha",sha)
