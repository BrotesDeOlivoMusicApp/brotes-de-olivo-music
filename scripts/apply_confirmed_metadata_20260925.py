from __future__ import annotations
import hashlib, json, sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB = Path("data/brotes_publica.sqlite")
VERSION = Path("data/version.json")
DATA_VERSION = "2026.09.25.4"

DISC_LINKS = {
    "D001": ("url_apple_music", "https://music.apple.com/es/album/allanad-los-caminos-single/1498042138"),
    "D011": ("url_apple_music", "https://music.apple.com/mx/album/el-forito-single/1497856151"),
    "D026": ("url_apple_music", "https://music.apple.com/us/album/sinfon%C3%ADa-de-las-vocales-single/1497729736"),
    "D032": ("url_deezer", "https://www.deezer.com/es/album/923416031"),
}
DURATIONS = {
    "C0361": 132,
    "C0362": 221,
    "C0363": 259,
    "C0364": 351,
    "C0365": 132,
    "C0366": 118,
    "C0367": 222,
    "C0368": 101,
    "C0369": 295,
    "C0370": 318,
    "C0371": 285,
    "C0372": 111,
    "C0373": 287,
    "C0374": 224,
    "C0375": 235,
    "C0376": 1020,
    "C0377": 220,
    "C0378": 295,
    "C0379": 307,
    "C0380": 238,
    "C0381": 592,
    "C0382": 216,
    "C0383": 121,
}

db = sqlite3.connect(DB)
try:
    db.execute("PRAGMA foreign_keys=ON")
    for disco_id, (field, url) in DISC_LINKS.items():
        db.execute(
            f"""UPDATE disco SET {field}=?
                WHERE disco_id=? AND ({field} IS NULL OR TRIM({field})='')""",
            (url, disco_id),
        )
    for cancion_id, seconds in DURATIONS.items():
        db.execute(
            "UPDATE cancion SET duracion_segundos=? WHERE cancion_id=? AND duracion_segundos IS NULL",
            (seconds, cancion_id),
        )
    now=datetime.now(timezone.utc).isoformat()
    db.execute("""INSERT INTO schema_migration(version,nombre,aplicada_en)
      VALUES(7,'completa_enlaces_y_duraciones_confirmadas',?)
      ON CONFLICT(version) DO UPDATE SET nombre=excluded.nombre, aplicada_en=excluded.aplicada_en""",(now,))
    db.execute("""INSERT INTO app_metadata(clave,valor) VALUES('data_version',?)
      ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor""",(DATA_VERSION,))
    db.execute("""INSERT INTO app_metadata(clave,valor) VALUES('schema_version','3')
      ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor""")
    for did,(field,url) in DISC_LINKS.items():
        assert db.execute(f"SELECT {field} FROM disco WHERE disco_id=?",(did,)).fetchone()[0] == url
    for cid,seconds in DURATIONS.items():
        assert db.execute("SELECT duracion_segundos FROM cancion WHERE cancion_id=?",(cid,)).fetchone()[0] == seconds
    assert db.execute("SELECT COUNT(*) FROM cancion WHERE disco_id IN ('D029','D030') AND duracion_segundos IS NULL").fetchone()[0] == 0
    assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
    assert not db.execute("PRAGMA foreign_key_check").fetchall()
    db.commit()
finally:
    db.close()

digest=hashlib.sha256(DB.read_bytes()).hexdigest()
VERSION.write_text(json.dumps({
 "dataVersion":DATA_VERSION,"schemaVersion":3,"file":"brotes_publica.sqlite",
 "sha256":digest,"date":"2026-09-25",
 "notes":"Completa 4 enlaces externos confirmados y 23 duraciones de 25 Años en Búsqueda Vol. I y II."
},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Distribución actualizada",DATA_VERSION)
