#!/usr/bin/env python3
"""Snapshot diario de estadisticas GitHub (solo API; nunca datos personales)."""
import base64
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

REPOSITORY = os.environ["GITHUB_REPOSITORY"]
API = "https://api.github.com/repos/" + REPOSITORY
TOKEN = os.environ["GITHUB_TOKEN"]
TRAFFIC_TOKEN = os.environ.get("GITHUB_STATS_TRAFFIC_TOKEN", "").strip()
TRACKED_FILES = [p.strip() for p in os.environ.get("GITHUB_STATS_TRACKED_FILES", "").split(",") if p.strip()]
NOW = dt.datetime.now(dt.timezone.utc)
ERRORS = []


def get(path, token=TOKEN):
    """Solo GET; no credenciales en salida, logs ni archivos."""
    req = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "User-Agent": "Brotes-GitHub-Statistics/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise FileNotFoundError(path) from exc
            if exc.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("HTTP " + str(exc.code)) from exc
        except (TimeoutError, urllib.error.URLError) as exc:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(type(exc).__name__) from exc


def optional(name, path, token=TOKEN):
    try:
        return {"status": "ok", "data": get(path, token)}
    except Exception as exc:
        ERRORS.append({"source": name, "error": str(exc)})
        return {"status": "error", "error": str(exc)}


def pages(name, path, max_pages=20):
    output = []
    for page in range(1, max_pages + 1):
        separator = "&" if "?" in path else "?"
        result = optional(name, path + separator + "per_page=100&page=" + str(page))
        if result["status"] != "ok":
            return {"status": "partial" if output else "error", "items": output}
        batch = result["data"]
        if not isinstance(batch, list):
            ERRORS.append({"source": name, "error": "unexpected_response"})
            return {"status": "partial", "items": output}
        output.extend(batch)
        if len(batch) < 100:
            return {"status": "ok", "items": output}
    ERRORS.append({"source": name, "error": "pagination_limit"})
    return {"status": "partial", "items": output}


def select_metadata():
    item = optional("repository", "")
    if item["status"] != "ok":
        return item
    info = item["data"]
    fields = ("id", "full_name", "visibility", "private", "archived",
              "default_branch", "stargazers_count", "subscribers_count",
              "watchers_count", "forks_count", "open_issues_count",
              "size", "created_at", "updated_at", "pushed_at")
    return {"status": "ok", "data": {k: info.get(k) for k in fields}}


def select_releases():
    result = pages("releases", "/releases")
    releases = []
    for release in result["items"]:
        tag = str(release.get("tag_name") or "")
        # Android se distribuye en Google Play, no en GitHub.
        # Excluir la Release COMPLETA: APK/AAB, mapeos, JSON y pruebas.
        if tag.lower().startswith("android-"):
            continue
        assets = []
        for a in release.get("assets", []):
            name = str(a.get("name") or "")
            # Cobertura adicional para APK/AAB fuera de tags android-*.
            if name.lower().endswith((".apk", ".aab")):
                continue
            assets.append({
                "id": a.get("id"), "name": a.get("name"),
                "size_bytes": a.get("size"), "downloads_total": a.get("download_count"),
                "created_at": a.get("created_at"), "updated_at": a.get("updated_at"),
            })
        releases.append({
            "id": release.get("id"), "tag": release.get("tag_name"),
            "draft": release.get("draft"), "prerelease": release.get("prerelease"),
            "published_at": release.get("published_at"), "assets": assets,
        })
    return {"status": result["status"], "items": releases,
            "asset_count": sum(len(r["assets"]) for r in releases),
            "excluded": {
                "release_tag_prefixes": ["android-"],
                "asset_extensions": [".apk", ".aab"],
                "reason": "Android distribution statistics belong to Google Play Console"
            }}


def select_actions():
    result = optional("actions", "/actions/runs?per_page=100")
    if result["status"] != "ok":
        return result
    data = result["data"]
    runs = []
    for r in data.get("workflow_runs", []):
        runs.append({
            "id": r.get("id"), "name": r.get("name"), "event": r.get("event"),
            "status": r.get("status"), "conclusion": r.get("conclusion"),
            "created_at": r.get("created_at"), "updated_at": r.get("updated_at"),
            "run_started_at": r.get("run_started_at"), "run_attempt": r.get("run_attempt"),
        })
    return {"status": "ok", "total_runs": data.get("total_count"),
            "recent_runs": runs}


def select_files():
    output = {}
    for path in TRACKED_FILES:
        name = "content:" + path
        try:
            data = get("/contents/" + urllib.parse.quote(path, safe="/"))
            row = {"status": "ok", "git_blob_sha": data.get("sha"),
                   "size_bytes": data.get("size"), "type": data.get("type")}
            if path.endswith(".json") and data.get("encoding") == "base64":
                try:
                    parsed = json.loads(base64.b64decode(data["content"]))
                    if isinstance(parsed, dict):
                        row["json_metadata"] = {
                            k: parsed[k] for k in ("version", "data_version",
                            "schema_version", "published_at", "updated_at")
                            if k in parsed and isinstance(parsed[k], (str, int, float, bool, type(None)))
                        }
                except (ValueError, KeyError, TypeError):
                    row["json_metadata"] = {"status": "unreadable"}
            output[path] = row
        except FileNotFoundError:
            output[path] = {"status": "not_found"}
        except Exception as exc:
            ERRORS.append({"source": name, "error": str(exc)})
            output[path] = {"status": "error", "error": str(exc)}
    return output


def select_traffic():
    if not TRAFFIC_TOKEN:
        return {"status": "requires_secret",
                "required_permission": "Administration:read",
                "secret_name": "GITHUB_STATS_TRAFFIC_TOKEN"}
    output = {}
    for name, path in (
        ("views", "/traffic/views?per=day"),
        ("clones", "/traffic/clones?per=day"),
        ("popular_paths", "/traffic/popular/paths"),
        ("popular_referrers", "/traffic/popular/referrers"),
    ):
        output[name] = optional("traffic:" + name, path, TRAFFIC_TOKEN)
    return {"status": "ok" if all(x["status"] == "ok" for x in output.values()) else "partial",
            "last_14_days_only": True, "endpoints": output}


def main():
    snapshot = {
        "schema_version": 1,
        "source": "github_rest_api",
        "repository": REPOSITORY,
        "date_utc": NOW.date().isoformat(),
        "collected_at_utc": NOW.isoformat(timespec="seconds"),
        "repository_metadata": select_metadata(),
        "release_assets": select_releases(),
        "workflow_runs": select_actions(),
        "tracked_files": select_files(),
        "traffic": select_traffic(),
        "errors": ERRORS,
        "limitations": {
            "raw_file_downloads": "unavailable",
            "github_pages_visitors": "unavailable",
            "github_traffic_history": "14_days",
            "release_downloads": "cumulative_by_asset_id",
        },
    }
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print("Repo:", REPOSITORY, "release assets:", snapshot["release_assets"]["asset_count"],
          "API errors:", len(ERRORS), "traffic:", snapshot["traffic"]["status"])
    if snapshot["repository_metadata"]["status"] != "ok" or snapshot["release_assets"]["status"] == "error":
        raise SystemExit("Failed to obtain essential GitHub metadata")


if __name__ == "__main__":
    main()
