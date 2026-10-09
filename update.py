#!/usr/bin/env python3
"""Fetch Hugging Face's top 10 trending models into trending.json.

    update.py [--message FILE]

Rewrites trending.json and writes a commit message describing what moved
since the previous file: models that entered the top 10 (announced as new),
models that left it, and rank changes. Prints the message too.
"""
import argparse
import json
import os
import urllib.request

URL = "https://huggingface.co/api/models?sort=trendingScore&limit=10"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trending.json")
FIELDS = ("trendingScore", "pipeline_tag", "likes", "downloads", "createdAt")


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "hf-trending"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        models = json.load(resp)
    return [{"rank": n, "id": m["id"], **{k: m.get(k) for k in FIELDS}}
            for n, m in enumerate(models[:10], 1)]


def message(old, new):
    before = {m["id"]: m["rank"] for m in old}
    after = {m["id"]: m["rank"] for m in new}
    entered = [m for m in new if m["id"] not in before]
    left = [m for m in old if m["id"] not in after]
    moved = [m for m in new if m["id"] in before and before[m["id"]] != m["rank"]]
    if entered:
        subject = f"Trending: {len(entered)} new in the top 10: " + ", ".join(m["id"] for m in entered)
    elif moved:
        subject = f"Trending: {len(moved)} rank change(s)"
    else:
        subject = "Trending: scores updated"
    body = [f"NEW  #{m['rank']} {m['id']} ({m['pipeline_tag']})" for m in entered]
    body += [f"OUT  {m['id']} (was #{m['rank']})" for m in left]
    body += [f"MOVE {m['id']} #{before[m['id']]} -> #{m['rank']}" for m in moved]
    return subject + ("\n\n" + "\n".join(body) if body else "") + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--message", help="write the commit message to this file")
    a = ap.parse_args()
    try:
        with open(DATA) as fh:
            old = json.load(fh)["models"]
    except FileNotFoundError:
        old = []
    new = fetch()
    if len(new) != 10:
        raise SystemExit(f"expected 10 models, got {len(new)}")
    msg = message(old, new)
    with open(DATA, "w") as fh:
        json.dump({"source": URL, "models": new}, fh, indent=2)
        fh.write("\n")
    if a.message:
        with open(a.message, "w") as fh:
            fh.write(msg)
    print(msg, end="")


if __name__ == "__main__":
    main()
