#!/usr/bin/env python3
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

NODE_BASE_URL = "https://node.freeclashnode.com/uploads/{year}/{month}/{index}-{date}.yaml"
V2RAY_BASE_URL = "https://node.freeclashnode.com/uploads/{year}/{month}/{index}-{date}.txt"
NODE_INDEX = 0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_url(url: str, timeout: int = 10) -> str | None:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
            if content.strip().startswith("<!DOCTYPE html") or content.strip().startswith("<html"):
                return None
            return content
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_nodes(date_str: str) -> dict:
    parts = date_str.split("-")
    year, month, day = parts[0], parts[1].zfill(2), parts[2].zfill(2)
    date_compact = f"{year}{month}{day}"

    clash_url = NODE_BASE_URL.format(year=year, month=month, index=NODE_INDEX, date=date_compact)
    v2ray_url = V2RAY_BASE_URL.format(year=year, month=month, index=NODE_INDEX, date=date_compact)

    return {
        "clash": fetch_url(clash_url),
        "v2ray": fetch_url(v2ray_url),
    }

def save_nodes(nodes: dict, output_dir: Path) -> bool:
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = False

    if nodes.get("clash"):
        (output_dir / "clash.yaml").write_text(nodes["clash"], encoding="utf-8")
        saved = True
    if nodes.get("v2ray"):
        (output_dir / "v2ray.txt").write_text(nodes["v2ray"], encoding="utf-8")
        saved = True
    return saved

def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("nodes")
    now = datetime.now(timezone.utc)
    beijing_now = now.astimezone(timezone(timedelta(hours=8)))
    date_str = f"{beijing_now.year}-{beijing_now.month}-{beijing_now.day}"

    nodes = fetch_nodes(date_str)
    if save_nodes(nodes, output_dir):
        print("OK")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
