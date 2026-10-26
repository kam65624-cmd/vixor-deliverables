#!/usr/bin/env python3
"""verify_manifest.py — package self-verifier for VIXOR TASK 22 final audit package.

Checks every entry registered in MANIFEST.json (files + evidence) against the REAL
bytes on disk (size + sha256). MANIFEST.json itself is excluded from registration
(it cannot contain its own hash) and is validated structurally (parses as JSON).
Exit 0 = all entries MATCH; exit 1 = any MISMATCH/MISSING. Prints one line per file.
Run from the package root:  python3 verify_manifest.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    mpath = os.path.join(HERE, "MANIFEST.json")
    try:
        man = json.load(open(mpath, encoding="utf-8"))
    except Exception as e:
        print(f"FATAL   MANIFEST.json unparseable: {e}")
        return 1

    total = 0
    bad = 0
    for section in ("files", "evidence"):
        entries = man.get(section, {})
        for name, meta in sorted(entries.items()):
            total += 1
            local = os.path.join(HERE, name)
            if not os.path.exists(local):
                bad += 1
                print(f"MISSING {name}")
                continue
            size = os.path.getsize(local)
            digest = sha256_of(local)
            if size == meta.get("bytes") and digest == meta.get("sha256"):
                print(f"OK      {name}  ({size} B)")
            else:
                bad += 1
                print(f"FAIL    {name}  ({size} B, sha256 {digest[:12]}… vs manifest "
                      f"{meta.get('bytes')} B / {str(meta.get('sha256'))[:12]}…)")

    print(f"RESULT: {'ALL MATCH' if bad == 0 else f'{bad}/{total} MISMATCH'} ({total} entries checked)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
