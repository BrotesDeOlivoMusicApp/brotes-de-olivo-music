#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

MEDIA_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".wav", ".flac", ".aac", ".ogg"}

def slug(text: str, max_len: int = 70) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-").lower()
    return (text or "sin-titulo")[:max_len].rstrip("-")

def extension_from_url(url: str) -> str:
    ext = Path(unquote(urlparse(url).path)).suffix.lower()
    return ext if ext in MEDIA_EXTENSIONS else ".bin"

def probe_duration(path: Path) -> float | None:
    try:
        cp = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        value = cp.stdout.strip()
        return round(float(value), 3) if value else None
    except Exception:
        return None

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def download(url: str, dest: Path, retries: int = 3, timeout: int = 60) -> tuple[str | None, int]:
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "BrotesDeOlivoMusicApp/1.0",
                    "Accept": "audio/*,video/*,application/octet-stream;q=0.8,*/*;q=0.1",
                },
            )
            with urlopen(req, timeout=timeout) as resp:
                content_type = (resp.headers.get_content_type() or "").lower()
                dest.parent.mkdir(parents=True, exist_ok=True)
                size = 0
                with dest.open("wb") as out:
                    while True:
                        chunk = resp.read(1024 * 1024)
                        if not chunk:
                            break
                        out.write(chunk)
                        size += len(chunk)
                if size < 1024:
                    raise RuntimeError(f"archivo demasiado pequeño ({size} bytes)")
                if content_type.startswith("text/") or content_type in {"application/json", "application/xml"}:
                    raise RuntimeError(f"tipo de contenido inesperado: {content_type}")
                return content_type or None, size
        except (HTTPError, URLError, TimeoutError, RuntimeError, OSError) as exc:
            last_error = str(exc)
            if dest.exists():
                dest.unlink()
            if attempt < retries:
                time.sleep(attempt * 2)
    raise RuntimeError(last_error or "error de descarga desconocido")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fuentes", default="fuentes.json")
    ap.add_argument("--salida", default="build")
    ap.add_argument("--inicio", type=int, default=0)
    ap.add_argument("--cantidad", type=int, default=10)
    ap.add_argument("--estricto", action="store_true")
    args = ap.parse_args()

    fuentes_path = Path(args.fuentes)
    salida = Path(args.salida)
    media_dir = salida / "media"
    salida.mkdir(parents=True, exist_ok=True)
    media_dir.mkdir(parents=True, exist_ok=True)

    doc = json.loads(fuentes_path.read_text(encoding="utf-8"))
    disponibles = [c for c in doc.get("canciones", []) if (c.get("url_origen") or "").strip()]
    lote = disponibles[args.inicio: args.inicio + args.cantidad]

    resultados = []
    errores = []

    for idx, c in enumerate(lote, start=args.inicio):
        url = c["url_origen"].strip()
        ext = extension_from_url(url)
        if ext == ".bin":
            ext = Path(c.get("archivo_origen") or "").suffix.lower() or ".bin"
        disco_id = c.get("disco_id") or "DXXX"
        cancion_id = c.get("cancion_id") or f"IDX{idx:04d}"
        pista = int(c.get("numero_pista") or 0)
        nombre = f"{disco_id}_{cancion_id}_{pista:02d}_{slug(c.get('titulo') or '')}{ext}"
        dest = media_dir / disco_id / nombre

        print(f"[{idx + 1}/{len(disponibles)}] {cancion_id} - {c.get('titulo')}")

        try:
            content_type, size = download(url, dest)
            mime_guess = mimetypes.guess_type(dest.name)[0]
            item = dict(c)
            item.update({
                "indice_fuente": idx,
                "archivo_release": nombre,
                "ruta_temporal": str(dest).replace("\\", "/"),
                "tipo_mime": content_type or mime_guess,
                "tamano_bytes": size,
                "sha256": sha256_file(dest),
                "duracion_real_segundos": probe_duration(dest),
                "estado_descarga": "ok",
            })
            resultados.append(item)
        except Exception as exc:
            errores.append({
                "indice_fuente": idx,
                "cancion_id": c.get("cancion_id"),
                "disco": c.get("disco"),
                "numero_pista": c.get("numero_pista"),
                "titulo": c.get("titulo"),
                "url_origen": url,
                "error": str(exc),
            })
            print(f"ERROR: {exc}", file=sys.stderr)

    manifest = {
        "version": 1,
        "inicio": args.inicio,
        "cantidad_solicitada": args.cantidad,
        "total_disponibles": len(disponibles),
        "procesadas": len(lote),
        "descargadas": len(resultados),
        "errores": len(errores),
        "canciones": resultados,
        "incidencias": errores,
    }
    (salida / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    total_bytes = sum(x["tamano_bytes"] for x in resultados)
    resumen = [
        f"Total con URL: {len(disponibles)}",
        f"Inicio: {args.inicio}",
        f"Solicitadas: {args.cantidad}",
        f"Procesadas: {len(lote)}",
        f"Descargadas: {len(resultados)}",
        f"Errores: {len(errores)}",
        f"Tamaño descargado: {total_bytes} bytes",
        f"Tamaño descargado MiB: {total_bytes / 1024 / 1024:.2f}",
    ]
    (salida / "resumen.txt").write_text("\n".join(resumen) + "\n", encoding="utf-8")
    print("\n".join(resumen))

    if args.estricto and errores:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
