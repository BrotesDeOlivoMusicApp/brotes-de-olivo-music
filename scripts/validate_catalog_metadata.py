#!/usr/bin/env python3
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "brotes_publica.sqlite"
VERSION = ROOT / "data" / "version.json"

info = json.loads(VERSION.read_text(encoding="utf-8"))
expected_version = str(info["dataVersion"])
expected_schema = int(info["schemaVersion"])
expected_sha = str(info["sha256"]).lower()

actual_sha = hashlib.sha256(DB.read_bytes()).hexdigest()
if actual_sha != expected_sha:
    raise SystemExit(
        f"SHA256 desincronizado: version.json={expected_sha} db={actual_sha}"
    )

con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
try:
    metadata = dict(
        con.execute(
            "SELECT clave, valor FROM app_metadata "
            "WHERE clave IN ('data_version','schema_version')"
        ).fetchall()
    )
    if metadata.get("data_version") != expected_version:
        raise SystemExit(
            "data_version desincronizado: "
            f"version.json={expected_version} db={metadata.get('data_version')}"
        )
    if int(metadata.get("schema_version", "0")) != expected_schema:
        raise SystemExit(
            "schema_version desincronizado: "
            f"version.json={expected_schema} db={metadata.get('schema_version')}"
        )
    if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        raise SystemExit("integrity_check falló")
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    if fk:
        raise SystemExit(f"foreign_key_check: {fk[:10]}")
finally:
    con.close()

print(
    f"OK catalogo {expected_version}; schema={expected_schema}; sha256={actual_sha}"
)
