#!/usr/bin/env python3
import sqlite3
from pathlib import Path
R=Path(__file__).resolve().parents[1]
con=sqlite3.connect(R/"data"/"brotes_publica.sqlite")
r=con.execute("select letra from cancion where cancion_id='C0205'").fetchone()
con.close()
if not r: raise SystemExit("C0205 no existe")
(R/"scripts"/"C0205_letra.txt").write_text(r[0] or "",encoding="utf-8")
