from __future__ import annotations
import hashlib, json, sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB=Path("data/brotes_publica.sqlite")
VERSION=Path("data/version.json")
DATA_VERSION="2026.09.25.2"
NOTE="Single independiente. Publicado originalmente por Polydor con referencia 20 62 089."

db=sqlite3.connect(DB)
try:
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("UPDATE disco SET anio=1972, observaciones=? WHERE disco_id='D011'",(NOTE,))
    now=datetime.now(timezone.utc).isoformat()
    db.execute("""INSERT INTO schema_migration(version,nombre,aplicada_en)
      VALUES(5,'corrige_el_forito_1972_y_observaciones',?)
      ON CONFLICT(version) DO UPDATE SET nombre=excluded.nombre""",(now,))
    db.execute("""INSERT INTO app_metadata(clave,valor) VALUES('data_version',?)
      ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor""",(DATA_VERSION,))
    db.execute("""INSERT INTO app_metadata(clave,valor) VALUES('schema_version','3')
      ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor""")
    assert db.execute("SELECT anio,observaciones FROM disco WHERE disco_id='D011'").fetchone()==(1972,NOTE)
    assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    assert not db.execute("PRAGMA foreign_key_check").fetchall()
    db.commit()
finally:
    db.close()

digest=hashlib.sha256(DB.read_bytes()).hexdigest()
VERSION.write_text(json.dumps({
 "dataVersion":DATA_VERSION,"schemaVersion":3,"file":"brotes_publica.sqlite",
 "sha256":digest,"date":"2026-09-25",
 "notes":"Corrige El Forito a 1972 y documenta que es un single independiente publicado originalmente por Polydor (20 62 089)."
},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Distribución actualizada",DATA_VERSION)
