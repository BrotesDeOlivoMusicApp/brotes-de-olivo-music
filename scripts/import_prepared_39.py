#!/usr/bin/env python3
import json,sqlite3,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"
CAND=R/"scripts"/"import_prepared_39.json"
cand=json.loads(CAND.read_text(encoding="utf-8"))
expected={
"C0118","C0119","C0120","C0121","C0122","C0123","C0124","C0125","C0126","C0127",
"C0128","C0129","C0132","C0147","C0148","C0149","C0150","C0151","C0152","C0153",
"C0154","C0155","C0156","C0157","C0158","C0159","C0171","C0172","C0173","C0174",
"C0175","C0176","C0177","C0178","C0179","C0180","C0181","C0182","C0183"}
if set(cand)!=expected:
    raise SystemExit(f"IDs inesperados: faltan={sorted(expected-set(cand))} sobran={sorted(set(cand)-expected)}")
for cid,txt in cand.items():
    if not txt or "[" not in txt or txt.count("[")!=txt.count("]"):
        raise SystemExit(f"Candidato inválido {cid}")
con=sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=87: raise SystemExit(f"Esperaba 87 canciones con acordes y hay {before}")
    for cid,txt in sorted(cand.items()):
        row=con.execute("select letra,acordes from cancion where cancion_id=?",(cid,)).fetchone()
        if not row: raise SystemExit(f"Falta {cid}")
        letra,acordes=row
        if (acordes or "").strip(): raise SystemExit(f"{cid} ya tiene acordes")
        plain=re.sub(r"\[[^\]\n]+\]","",txt)
        if plain!=(letra or ""): raise SystemExit(f"{cid}: texto subyacente no coincide con letra V11")
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    con.commit()
    if con.execute("pragma integrity_check").fetchone()[0]!="ok":
        raise SystemExit("integrity_check falló")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk: raise SystemExit(f"foreign_key_check: {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=126: raise SystemExit(f"Esperaba 126 y hay {after}")
finally:
    con.close()
info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.10.01.2":
    raise SystemExit(f"Versión inesperada {info.get('dataVersion')}")
sha=hashlib.sha256(DB.read_bytes()).hexdigest()
info["dataVersion"]="2026.10.01.3"
info["sha256"]=sha
info["date"]="2026-10-01"
info["notes"]="Sexto lote de acordes: 39 canciones preparadas importadas. Total acumulado: 126 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK 39 importadas; total 126; dataVersion",info["dataVersion"],"sha",sha)
