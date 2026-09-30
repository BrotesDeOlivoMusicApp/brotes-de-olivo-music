#!/usr/bin/env python3
import json,sqlite3,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"; V=R/"data"/"version.json"
cand={}
for i in range(1,5):
  cand.update(json.loads((R/"scripts"/f"chords_import_batch3_{i}.json").read_text(encoding="utf-8")))
if len(cand)!=31: raise SystemExit(f"Esperaba 31 candidatos y hay {len(cand)}")
con=sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON")
try:
  current=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
  if current!=25: raise SystemExit(f"Esperaba 25 acordes previos y hay {current}")
  missing=[cid for cid in cand if con.execute("select 1 from cancion where cancion_id=?",(cid,)).fetchone() is None]
  if missing: raise SystemExit(f"IDs inexistentes: {missing}")
  for cid,txt in cand.items(): con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
  con.commit()
  if con.execute("pragma integrity_check").fetchone()[0]!="ok": raise SystemExit("integrity_check falló")
  fk=con.execute("pragma foreign_key_check").fetchall()
  if fk: raise SystemExit(f"foreign_key_check: {fk[:5]}")
  total=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
  if total!=56: raise SystemExit(f"Esperaba 56 acordes y hay {total}")
finally: con.close()
info=json.loads(V.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.09.30.5": raise SystemExit(f"Versión base inesperada: {info.get('dataVersion')}")
sha=hashlib.sha256(DB.read_bytes()).hexdigest()
info["dataVersion"]="2026.09.30.6"; info["sha256"]=sha; info["date"]="2026-09-30"
info["notes"]="Tercer lote de acordes: 31 canciones aprobadas. Total acumulado: 56 canciones con acordes."
V.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK",len(cand),"nuevas; total",56,"version",info["dataVersion"],"sha",sha)
