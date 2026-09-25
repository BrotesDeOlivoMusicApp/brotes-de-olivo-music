from __future__ import annotations
import hashlib, json, sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH=Path("data/brotes_publica.sqlite")
VERSION_PATH=Path("data/version.json")
DATA_VERSION="2026.09.25.1"
PAIRS=(("C0001","C0130"),("C0002","C0138"),("C0342","C0156"),("C0343","C0155"))
DISC_NOTES={
 "D001":"Single promocional de «El Evangelio según San Juan».",
 "D026":"Single promocional de «Entre el Cielo y la Tierra».",
}
TEXT_COLUMNS=("letra","url_audio_web","isrc","grupo_propietario","estudio_grabacion",
              "artista_principal","url_youtube","url_spotify","url_otro","tipo_contenido")

def has_column(db,table,column):
    return any(r[1]==column for r in db.execute(f"PRAGMA table_info({table})"))

def ensure_schema(db):
    if not has_column(db,"disco","observaciones"):
        db.execute("ALTER TABLE disco ADD COLUMN observaciones TEXT")
    db.execute("DROP VIEW IF EXISTS v_disco_resumen")
    db.execute("""CREATE VIEW v_disco_resumen AS
      SELECT d.disco_id,d.titulo,d.anio,COUNT(c.cancion_id) AS numero_canciones,
      CASE WHEN COUNT(c.cancion_id)=0 THEN NULL
           WHEN SUM(CASE WHEN c.duracion_segundos IS NULL THEN 1 ELSE 0 END)>0 THEN NULL
           ELSE SUM(c.duracion_segundos) END AS duracion_total_segundos,
      d.upc_ean,d.referencia,d.portada_url,d.url_web_oficial,d.url_youtube_music,
      d.url_spotify,d.url_apple_music,d.url_deezer,d.observaciones
      FROM disco d LEFT JOIN cancion c ON c.disco_id=d.disco_id GROUP BY d.disco_id""")

def next_id(db,table,column,sample):
    i=len(sample)
    while i>0 and sample[i-1].isdigit(): i-=1
    prefix=sample[:i] or "ID"; width=max(5,len(sample)-i); maximum=0
    for (value,) in db.execute(f"SELECT {column} FROM {table} WHERE {column} LIKE ?",(f"{prefix}%",)):
        if isinstance(value,str) and value.startswith(prefix):
            suffix=value[len(prefix):]
            if suffix.isdigit():
                maximum=max(maximum,int(suffix)); width=max(width,len(suffix))
    return f"{prefix}{maximum+1:0{width}d}"

def complete_song(db,target,source):
    for col in TEXT_COLUMNS:
        db.execute(f"""UPDATE cancion AS t
          SET {col}=(SELECT s.{col} FROM cancion s WHERE s.cancion_id=?)
          WHERE t.cancion_id=? AND (t.{col} IS NULL OR TRIM(t.{col})='')
          AND EXISTS(SELECT 1 FROM cancion s WHERE s.cancion_id=? AND s.{col} IS NOT NULL AND TRIM(s.{col})<>'')""",
          (source,target,source))
    db.execute("""UPDATE cancion AS t
      SET duracion_segundos=(SELECT s.duracion_segundos FROM cancion s WHERE s.cancion_id=?)
      WHERE t.cancion_id=? AND t.duracion_segundos IS NULL
      AND EXISTS(SELECT 1 FROM cancion s WHERE s.cancion_id=? AND s.duracion_segundos IS NOT NULL)""",
      (source,target,source))
    for cid,kind,participant,order_no in db.execute(
        "SELECT credito_id,tipo_credito_id,participante_id,orden FROM credito_cancion WHERE cancion_id=? ORDER BY tipo_credito_id,orden,participante_id",(source,)).fetchall():
        if not db.execute("SELECT 1 FROM credito_cancion WHERE cancion_id=? AND tipo_credito_id=? AND participante_id=? AND orden=? LIMIT 1",(target,kind,participant,order_no)).fetchone():
            db.execute("INSERT INTO credito_cancion(credito_id,cancion_id,tipo_credito_id,participante_id,orden) VALUES(?,?,?,?,?)",
                       (next_id(db,"credito_cancion","credito_id",cid),target,kind,participant,order_no))
    for rid,classification in db.execute(
        "SELECT relacion_id,clasificacion_id FROM cancion_clasificacion WHERE cancion_id=? ORDER BY clasificacion_id",(source,)).fetchall():
        if not db.execute("SELECT 1 FROM cancion_clasificacion WHERE cancion_id=? AND clasificacion_id=? LIMIT 1",(target,classification)).fetchone():
            db.execute("INSERT INTO cancion_clasificacion(relacion_id,cancion_id,clasificacion_id) VALUES(?,?,?)",
                       (next_id(db,"cancion_clasificacion","relacion_id",rid),target,classification))

def main():
    db=sqlite3.connect(DB_PATH)
    try:
        db.execute("PRAGMA foreign_keys=ON"); ensure_schema(db)
        for disc_id,note in DISC_NOTES.items():
            db.execute("UPDATE disco SET observaciones=? WHERE disco_id=? AND (observaciones IS NULL OR TRIM(observaciones)='')",(note,disc_id))
        for target,source in PAIRS: complete_song(db,target,source)
        now=datetime.now(timezone.utc).isoformat()
        db.execute("""INSERT INTO schema_migration(version,nombre,aplicada_en)
          VALUES(4,'observaciones_disco_y_completar_singles_promocionales',?)
          ON CONFLICT(version) DO UPDATE SET nombre=excluded.nombre""",(now,))
        db.execute("""INSERT INTO app_metadata(clave,valor) VALUES('data_version',?)
          ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor""",(DATA_VERSION,))
        db.execute("""INSERT INTO app_metadata(clave,valor) VALUES('schema_version','3')
          ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor""")
        assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        assert not db.execute("PRAGMA foreign_key_check").fetchall()
        db.commit()
    finally: db.close()
    digest=hashlib.sha256(DB_PATH.read_bytes()).hexdigest()
    VERSION_PATH.write_text(json.dumps({
      "dataVersion":DATA_VERSION,"schemaVersion":3,"file":"brotes_publica.sqlite",
      "sha256":digest,"date":"2026-09-25",
      "notes":"Añade observaciones de singles promocionales y completa metadatos faltantes de sus canciones equivalentes."
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Distribución actualizada",DATA_VERSION)
if __name__=="__main__": main()
