#!/usr/bin/env python3
import json, sqlite3, hashlib
from pathlib import Path

R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"

cand={}
for i in range(1,4):
    cand.update(json.loads((R/"scripts"/f"import_prepared_27_{i}.json").read_text(encoding="utf-8")))

if len(cand)!=27:
    raise SystemExit(f"Esperaba 27 candidatos y hay {len(cand)}")
if any(not (v or "").strip() for v in cand.values()):
    raise SystemExit("Hay candidatos vacíos")

con=sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=56:
        raise SystemExit(f"Esperaba 56 canciones con acordes antes de importar y hay {before}")
    missing=[cid for cid in cand if con.execute("select 1 from cancion where cancion_id=?",(cid,)).fetchone() is None]
    if missing:
        raise SystemExit(f"IDs inexistentes: {missing}")
    already=[cid for cid in cand if con.execute("select trim(coalesce(acordes,'')) from cancion where cancion_id=?",(cid,)).fetchone()[0]]
    if already:
        raise SystemExit(f"Ya tenían acordes y no deben sobrescribirse: {already}")
    for cid,txt in cand.items():
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    con.commit()
    if con.execute("pragma integrity_check").fetchone()[0]!="ok":
        raise SystemExit("PRAGMA integrity_check falló")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk:
        raise SystemExit(f"PRAGMA foreign_key_check falló: {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=83:
        raise SystemExit(f"Esperaba 83 canciones con acordes al final y hay {after}")
finally:
    con.close()

info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.09.30.6":
    raise SystemExit(f"dataVersion inesperada: {info.get('dataVersion')}")
sha=hashlib.sha256(DB.read_bytes()).hexdigest()
info["dataVersion"]="2026.10.01.1"
info["sha256"]=sha
info["date"]="2026-10-01"
info["notes"]="Cuarto lote de acordes: 27 canciones preparadas importadas. Total acumulado: 83 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"OK: 27 importadas; total 83; dataVersion {info['dataVersion']}; sha256 {sha}")
