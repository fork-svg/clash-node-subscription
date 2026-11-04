#!/usr/bin/env python3
"""
fetch_nodes.py
从 clash-free-node 网站抓取每日更新的免费节点
"""

import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path


# 节点源 URL 格式
# https://node.freeclashnode.com/uploads/{year}/{month}/{index}-{year}{month}{day}.yaml
# https://node.freeclashnode.com/uploads/{year}/{month}/{index}-{year}{month}{day}.txt

NODE_BASE_URL = "https://node.freeclashnode.com/uploads/{year}/{month}/{index}-{date}.yaml"
V2RAY_BASE_URL = "https://node.freeclashnode.com/uploads/{year}/{month}/{index}-{date}.txt"

# 要抓取的节点索引 (0-4，对应 node0-node4)
# 用户要求 node1，对应 index=0（第一个）
NODE_INDEX = 0

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_url(url: str, timeout: int = 10) -> str | None:
    """Fetch content from URL."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
            # 检查是否返回了错误页面（HTML 而不是配置）
            if content.strip().startswith("<!DOCTYPE html") or content.strip().startswith("<html"):
                return None
            return content
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_nodes(date_str: str) -> dict:
    """Fetch Clash and V2Ray nodes for the given date.

    Args:
        date_str: Date string in format "YYYY-M-D" (e.g., "2026-11-4")

    Returns:
        Dictionary with 'clash' and 'v2ray' keys containing node data
    """
    # Parse date
    parts = date_str.split("-")
    year = parts[0]
    month = parts[1].zfill(2)
    day = parts[2].zfill(2)
    date_compact = f"{year}{month}{day}"

    # Build URLs
    clash_url = NODE_BASE_URL.format(
        year=year, month=month, index=NODE_INDEX, date=date_compact
    )
    v2ray_url = V2RAY_BASE_URL.format(
        year=year, month=month, index=NODE_INDEX, date=date_compact
    )

    print(f"Fetching Clash config from: {clash_url}")
    clash_content = fetch_url(clash_url)

    print(f"Fetching V2Ray config from: {v2ray_url}")
    v2ray_content = fetch_url(v2ray_url)

    return {
        "clash": clash_content,
        "v2ray": v2ray_content,
        "clash_url": clash_url,
        "v2ray_url": v2ray_url,
    }


def save_nodes(nodes: dict, output_dir: Path) -> bool:
    """Save nodes to files.

    Returns:
        True if at least one node was saved successfully
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = False

    if nodes.get("clash"):
        clash_file = output_dir / "clash.yaml"
        clash_file.write_text(nodes["clash"], encoding="utf-8")
        print(f"✅ Saved Clash config to: {clash_file}")
        saved = True
    else:
        print("❌ Failed to fetch Clash config")

    if nodes.get("v2ray"):
        v2ray_file = output_dir / "v2ray.txt"
        v2ray_file.write_text(nodes["v2ray"], encoding="utf-8")
        print(f"✅ Saved V2Ray config to: {v2ray_file}")
        saved = True
    else:
        print("❌ Failed to fetch V2Ray config")

    return saved


def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("nodes")

    # Use today's date in Beijing timezone (UTC+8)
    now = datetime.now(timezone.utc)
    beijing_tz = timezone(timedelta(hours=8))
    beijing_now = now.astimezone(beijing_tz)

    # Format date as "YYYY-M-D" (no leading zeros for month and day)
    date_str = f"{beijing_now.year}-{beijing_now.month}-{beijing_now.day}"

    print(f"=" * 60)
    print(f"Fetching nodes for: {date_str}")
    print(f"=" * 60)

    nodes = fetch_nodes(date_str)

    if save_nodes(nodes, output_dir):
        print("\n" + "=" * 60)
        print("SUCCESS: Nodes updated")
        print("=" * 60)
        print(f"\nClash URL: {nodes.get('clash_url', 'N/A')}")
        print(f"V2Ray URL: {nodes.get('v2ray_url', 'N/A')}")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("FAILED: Could not fetch any nodes")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
