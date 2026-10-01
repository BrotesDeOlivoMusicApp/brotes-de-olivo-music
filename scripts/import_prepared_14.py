#!/usr/bin/env python3
import json, sqlite3, hashlib, re
from pathlib import Path

R=Path(__file__).resolve().parents[1]
DB=R/"data"/"brotes_publica.sqlite"
VER=R/"data"/"version.json"
cand=json.loads((R/"scripts"/"analysis_batch20e_candidates.json").read_text(encoding="utf-8"))
expected={"C0102","C0104","C0106","C0107","C0108","C0109","C0110","C0111","C0112","C0113","C0114","C0115","C0116","C0117"}
if set(cand)!=expected or len(cand)!=14:
    raise SystemExit(f"Conjunto inesperado: {sorted(cand)}")

info=json.loads(VER.read_text(encoding="utf-8"))
if info.get("dataVersion")!="2026.10.01.5":
    raise SystemExit(f"Versión inesperada {info.get('dataVersion')}")

con=sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    before=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if before!=191:
        raise SystemExit(f"Esperaba 191 canciones con acordes y hay {before}")
    for cid,txt in sorted(cand.items()):
        row=con.execute("select letra,acordes from cancion where cancion_id=?",(cid,)).fetchone()
        if not row: raise SystemExit(f"Falta {cid}")
        if (row[1] or "").strip(): raise SystemExit(f"{cid} ya tiene acordes")
        if txt.count("[")!=txt.count("]"): raise SystemExit(f"{cid}: corchetes desbalanceados")
        if "[" not in txt: raise SystemExit(f"{cid}: sin acordes")
        plain=re.sub(r"\[[^\]\n]+\]","",txt)
        if plain!=(row[0] or ""): raise SystemExit(f"{cid}: letra no coincide con V11")
        con.execute("update cancion set acordes=? where cancion_id=?",(txt,cid))
    next_version="2026.10.01.6"
    con.execute("update app_metadata set valor=? where clave='data_version'",(next_version,))
    con.commit()
    if con.execute("pragma integrity_check").fetchone()[0]!="ok": raise SystemExit("integrity_check")
    fk=con.execute("pragma foreign_key_check").fetchall()
    if fk: raise SystemExit(f"foreign_key_check {fk[:10]}")
    after=con.execute("select count(*) from cancion where trim(coalesce(acordes,''))<>''").fetchone()[0]
    if after!=205: raise SystemExit(f"Esperaba 205 y hay {after}")
    stored=con.execute("select valor from app_metadata where clave='data_version'").fetchone()
    if not stored or stored[0]!=next_version: raise SystemExit(f"data_version interno: {stored}")
finally:
    con.close()

info["dataVersion"]="2026.10.01.6"
info["sha256"]=hashlib.sha256(DB.read_bytes()).hexdigest()
info["date"]="2026-10-01"
info["notes"]="Noveno lote de acordes: 14 canciones preparadas importadas. Total acumulado: 205 canciones con acordes."
VER.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("OK 14 importadas; total 205; dataVersion",info["dataVersion"],"sha",info["sha256"])
