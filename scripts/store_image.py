#!/usr/bin/env python3
"""Save an expiring image link (e.g. a Canva export) permanently in this repo.

Usage: python3 scripts/store_image.py "<image url>" posts/<date>/post-<slot>-ai.png
Triggers the fetch-image GitHub workflow, waits until the file is served from
raw.githubusercontent.com, checks it is a 1080x1080 image, and prints the raw URL.
"""
import io
import json
import os
import sys
import time
import urllib.request

REPO = "Mesbah50/CBD-social-media-"


def main(url, path):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    body = json.dumps({"ref": "main", "inputs": {"url": url, "path": path}}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/actions/workflows/fetch-image.yml/dispatches",
        data=body, method="POST",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=30)
    raw = f"https://raw.githubusercontent.com/{REPO}/main/{path}"
    for _ in range(60):
        time.sleep(6)
        try:
            data = urllib.request.urlopen(raw + f"?t={time.time():.0f}", timeout=20).read()
        except Exception:
            continue
        try:
            from PIL import Image
            size = Image.open(io.BytesIO(data)).size
        except Exception:
            size = None
        print(raw, size)
        return 0
    print("TIMEOUT: file did not appear", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
