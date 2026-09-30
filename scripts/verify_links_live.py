#!/usr/bin/env python3
"""
verify_links_live.py — check every distinct direct link against a LIVE ARES server
==================================================================================
Complements scripts/check_resource_links.py (which verifies against the mounted
reference disk image, offline). This one asks a running server:
  - Kolibri links  -> Kolibri content API: node exists and `available` is true
  - Web-module links -> HTTP GET of /modules/<path> returns 200

Links are rewritten from http://ares.local[:8069]/... to the server given, e.g.
  python3 scripts/verify_links_live.py --base https://demo.aresedu.dev \
      --kolibri-api https://demo.aresedu.dev/kolibri/api/content/contentnode/
For a school server on its own network (Kolibri on port 8069):
  python3 scripts/verify_links_live.py --base http://ares.local \
      --kolibri-api http://ares.local:8069/api/content/contentnode/

Read-only; one request per distinct link, 8 at a time. Exit 1 if any link fails.
"""
import argparse
import glob
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect(paths):
    files = []
    for t in paths or [os.path.join(ROOT, "data", "outputs", "v2")]:
        files += glob.glob(os.path.join(t, "**", "*_data.json"), recursive=True) if os.path.isdir(t) else [t]
    links = {}
    for f in files:
        for L in json.load(open(f))["LESSONS"]:
            for pr in L["resourceLinks"].values():
                for s in ("video", "reading"):
                    r = pr.get(s)
                    if r and r.get("direct_url"):
                        links.setdefault(r["direct_url"], r["title"])
    return links


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "cbe-link-verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(1_000_000)
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # network error, timeout
        return None, str(e).encode()


def check(url, base, kolibri_api):
    u = urlparse(url)
    if ":8069" in u.netloc or "/learn/" in u.path:
        node = url.rstrip("/").rsplit("/", 1)[-1]
        status, body = fetch(f"{kolibri_api.rstrip('/')}/{node}/")
        if status != 200:
            return f"kolibri node {node}: HTTP {status}"
        try:
            if not json.loads(body).get("available", False):
                return f"kolibri node {node}: available=false"
        except ValueError:
            return f"kolibri node {node}: unreadable API response"
        return ""
    status, _ = fetch(base.rstrip("/") + u.path + (f"?{u.query}" if u.query else ""))
    return "" if status == 200 else f"HTTP {status}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="server root replacing http://ares.local")
    ap.add_argument("--kolibri-api", required=True, help="Kolibri contentnode API root")
    ap.add_argument("paths", nargs="*")
    a = ap.parse_args()
    links = collect(a.paths)
    kinds = {"kolibri": 0, "web": 0}
    for u in links:
        kinds["kolibri" if ":8069" in u else "web"] += 1
    print(f"verify_links_live: {len(links)} distinct direct links ({kinds['kolibri']} Kolibri, {kinds['web']} web) against {a.base}")
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(lambda u: (u, check(u, a.base, a.kolibri_api)), links))
    bad = [(u, why) for u, why in results if why]
    for u, why in bad:
        print(f"  FAIL {why}  {links[u][:60]!r}  {u}")
    print(f"  {len(links) - len(bad)} OK, {len(bad)} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
