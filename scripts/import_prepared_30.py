#!/usr/bin/env python3
import json, sqlite3, hashlib, re
from pathlib import Path

R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"

a=json.loads((R/"scripts"/"analysis_batch20c_candidates.json").read_text(encoding="utf-8"))
b=json.loads((R/"scripts"/"analysis_batch20d_candidates.json").read_text(encoding="utf-8"))
cand={**a,**b}

expected={
"C0067","C0068","C0069","C0070","C0071","C0072","C0074","C0075","C0076","C0077",
"C0078","C0079","C0080","C0081","C0082","C0083","C0084","C0086","C0088","C0090",
"C0091","C0092","C0093","C0094","C0095","C0097","C0098","C0099","C0100","C0101"
}
if set(cand)!=expected:
    raise SystemExit(f"IDs inesperados: faltan={sorted(expected-set(cand))} sobran={sorted(set(cand)-expected)}")
if len(cand)!=30:
    raise SystemExit(f"Esperaba 30 y hay {len(cand)}")

info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.10.01.4":
    raise SystemExit(f"Versión inesperada {info.get('dataVersion')}")

con=sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=161:
        raise SystemExit(f"Esperaba 161 canciones con acordes y hay {before}")
    for cid,txt in sorted(cand.items()):
        row=con.execute("select letra,acordes from cancion where cancion_id=?",(cid,)).fetchone()
        if not row:
            raise SystemExit(f"Falta {cid}")
        if (row[1] or "").strip():
            raise SystemExit(f"{cid} ya tiene acordes")
        if txt.count("[")!=txt.count("]"):
            raise SystemExit(f"{cid}: corchetes desbalanceados")
        if "[" not in txt:
            raise SystemExit(f"{cid}: candidato sin acordes")
        plain=re.sub(r"\[[^\]\n]+\]","",txt)
        if plain!=(row[0] or ""):
            raise SystemExit(f"{cid}: letra no coincide exactamente con V11")
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    next_version="2026.10.01.5"
    con.execute("update app_metadata set valor=? where clave='data_version'",(next_version,))
    con.commit()

    if con.execute("pragma integrity_check").fetchone()[0]!="ok":
        raise SystemExit("integrity_check")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk:
        raise SystemExit(f"foreign_key_check {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=191:
        raise SystemExit(f"Esperaba 191 canciones con acordes y hay {after}")
    stored=con.execute("select valor from app_metadata where clave='data_version'").fetchone()
    if not stored or stored[0]!=next_version:
        raise SystemExit(f"data_version interno no actualizado: {stored}")
finally:
    con.close()

info["dataVersion"]="2026.10.01.5"
info["sha256"]=hashlib.sha256(DB.read_bytes()).hexdigest()
info["date"]="2026-10-01"
info["notes"]="Octavo lote de acordes: 30 canciones preparadas importadas. Total acumulado: 191 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK 30 importadas; total 191; dataVersion",info["dataVersion"],"sha",info["sha256"])
