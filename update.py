#!/usr/bin/env python3
"""Fetch Hugging Face's top 10 trending model ids into trending.json.

    update.py [--message FILE]

Rewrites trending.json — just the model ids in Hugging Face's trending
order — and writes a commit message describing what moved since the
previous file: models that entered the top 10 (announced as new), models
that left it, and rank changes. Prints the message too.
"""
import argparse
import json
import os
import urllib.request

URL = "https://huggingface.co/api/models?sort=trendingScore&limit=10"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trending.json")


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "hf-trending"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        models = json.load(resp)
    return [{"id": m["id"]} for m in models[:10]]


def message(old, new):
    before = {m["id"]: n for n, m in enumerate(old, 1)}
    after = {m["id"]: n for n, m in enumerate(new, 1)}
    entered = [m for m in new if m["id"] not in before]
    left = [m for m in old if m["id"] not in after]
    moved = [m for m in new if m["id"] in before and before[m["id"]] != after[m["id"]]]
    if entered:
        subject = f"Trending: {len(entered)} new in the top 10: " + ", ".join(m["id"] for m in entered)
    elif moved:
        subject = f"Trending: {len(moved)} rank change(s)"
    else:
        subject = "Trending: order updated"
    body = [f"NEW  #{after[m['id']]} {m['id']}" for m in entered]
    body += [f"OUT  {m['id']} (was #{before[m['id']]})" for m in left]
    body += [f"MOVE {m['id']} #{before[m['id']]} -> #{after[m['id']]}" for m in moved]
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
