#!/usr/bin/env python3
# Reusable repair for catalogue metadata.
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "brotes_publica.sqlite"
VERSION = ROOT / "data" / "version.json"

info = json.loads(VERSION.read_text(encoding="utf-8"))
target_version = str(info["dataVersion"])
target_schema = int(info["schemaVersion"])

con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    row = con.execute(
        "SELECT valor FROM app_metadata WHERE clave='data_version' LIMIT 1"
    ).fetchone()
    if row is None:
        raise SystemExit("Falta app_metadata.data_version")

    previous = str(row[0])
    if previous != target_version:
        con.execute(
            "UPDATE app_metadata SET valor=? WHERE clave='data_version'",
            (target_version,),
        )

    schema = con.execute(
        "SELECT valor FROM app_metadata WHERE clave='schema_version' LIMIT 1"
    ).fetchone()
    if schema is None or int(schema[0]) != target_schema:
        raise SystemExit(
            f"schema_version interno inesperado: {schema[0] if schema else None}; "
            f"manifest={target_schema}"
        )

    con.commit()

    stored = con.execute(
        "SELECT valor FROM app_metadata WHERE clave='data_version' LIMIT 1"
    ).fetchone()[0]
    if str(stored) != target_version:
        raise SystemExit(
            f"No se pudo actualizar data_version interno: {stored} != {target_version}"
        )

    if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise SystemExit("integrity_check falló")

    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    if fk:
        raise SystemExit(f"foreign_key_check: {fk[:10]}")
finally:
    con.close()

sha = hashlib.sha256(DB.read_bytes()).hexdigest()
info["sha256"] = sha
VERSION.write_text(
    json.dumps(info, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(
    f"OK data_version {previous} -> {target_version}; "
    f"schema={target_schema}; sha256={sha}"
)
