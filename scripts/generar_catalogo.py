#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

def limpia(valor):
    if valor is None:
        return None
    if isinstance(valor, str):
        valor = valor.strip()
        return valor or None
    return valor

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifests", default="manifests")
    ap.add_argument("--salida", default="catalogo.json")
    ap.add_argument("--repo", default="BrotesDeOlivoMusicApp/brotes-de-olivo-music")
    ap.add_argument("--tag", default="discografia-v1")
    args = ap.parse_args()

    manifest_dir = Path(args.manifests)
    canciones = []
    incidencias = []

    files = sorted(manifest_dir.glob("manifest-*.json"))
    if not files:
        raise SystemExit("No se encontraron manifest-*.json")

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        canciones.extend(data.get("canciones", []))
        incidencias.extend(data.get("incidencias", []))

    por_id = {}
    for c in canciones:
        cid = limpia(c.get("cancion_id"))
        if not cid:
            continue
        por_id[cid] = c

    salida_canciones = []
    for cid, c in sorted(
        por_id.items(),
        key=lambda item: (
            item[1].get("disco_id") or "",
            int(item[1].get("numero_pista") or 0),
            item[0],
        ),
    ):
        archivo = c["archivo_release"]
        item = {
            "id": cid,
            "titulo": c.get("titulo") or cid,
            "archivo": archivo,
            "url": f"https://github.com/{args.repo}/releases/download/{args.tag}/{quote(archivo)}",
            "tipo": c.get("tipo_mime") or "application/octet-stream",
            "version": 1,
        }

        opcionales = {
            "isrc": limpia(c.get("isrc")),
            "disco": limpia(c.get("disco")),
            "anio": c.get("anio"),
            "numero_pista": c.get("numero_pista"),
            "url_origen": limpia(c.get("url_origen")),
            "duracion_segundos": (
                int(round(c["duracion_real_segundos"]))
                if c.get("duracion_real_segundos") is not None
                else c.get("duracion_segundos")
            ),
            "tamano_bytes": c.get("tamano_bytes"),
            "sha256": limpia(c.get("sha256")),
        }
        for k, v in opcionales.items():
            if v is not None:
                item[k] = v

        salida_canciones.append(item)

    catalogo = {
        "version": 1,
        "fecha_actualizacion": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "canciones": salida_canciones,
    }

    Path(args.salida).write_text(
        json.dumps(catalogo, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Manifiestos: {len(files)}")
    print(f"Canciones únicas catalogadas: {len(salida_canciones)}")
    print(f"Incidencias acumuladas: {len(incidencias)}")
    if incidencias:
        for i in incidencias:
            print(f"INCIDENCIA: {i}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
