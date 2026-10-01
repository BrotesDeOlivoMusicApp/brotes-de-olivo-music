#!/usr/bin/env python3
import json, sqlite3, hashlib, re
from pathlib import Path

R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"
cand=json.loads((R/"scripts"/"analysis_batch30f_candidates.json").read_text(encoding="utf-8"))
expected={"C0209","C0210","C0211","C0212","C0213","C0214","C0215","C0216","C0218","C0219"}
if set(cand)!=expected or len(cand)!=10:
    raise SystemExit(f"Conjunto inesperado: {sorted(cand)}")

info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.10.01.6":
    raise SystemExit(f"Versión inesperada {info.get('dataVersion')}")

con=sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=205:
        raise SystemExit(f"Esperaba 205 canciones con acordes y hay {before}")
    for cid,txt in sorted(cand.items()):
        row=con.execute("select letra,acordes from cancion where cancion_id=?",(cid,)).fetchone()
        if not row: raise SystemExit(f"Falta {cid}")
        if (row[1] or "").strip(): raise SystemExit(f"{cid} ya tiene acordes")
        if txt.count("[")!=txt.count("]"): raise SystemExit(f"{cid}: corchetes desbalanceados")
        if "[" not in txt: raise SystemExit(f"{cid}: sin acordes")
        plain=re.sub(r"\[[^\]\n]+\]","",txt)
        if plain!=(row[0] or ""): raise SystemExit(f"{cid}: letra no coincide con V11")
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    next_version="2026.10.01.7"
    con.execute("update app_metadata set valor=? where clave='data_version'",(next_version,))
    con.commit()
    if con.execute("pragma integrity_check").fetchone()[0]!="ok": raise SystemExit("integrity_check")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk: raise SystemExit(f"foreign_key_check {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=215: raise SystemExit(f"Esperaba 215 y hay {after}")
    stored=con.execute("select valor from app_metadata where clave='data_version'").fetchone()
    if not stored or stored[0]!=next_version: raise SystemExit(f"data_version interno: {stored}")
finally:
    con.close()

info["dataVersion"]="2026.10.01.7"
info["sha256"]=hashlib.sha256(DB.read_bytes()).hexdigest()
info["date"]="2026-10-01"
info["notes"]="Décimo lote de acordes: 10 canciones preparadas importadas. Total acumulado: 215 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK 10 importadas; total 215; dataVersion",info["dataVersion"],"sha",info["sha256"])
