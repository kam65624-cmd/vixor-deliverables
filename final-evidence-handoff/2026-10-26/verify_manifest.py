#!/usr/bin/env python3
"""Self-verifier for this evidence package (added 2026-10-27, F1 correction).
Run: python3 verify_manifest.py   -> exit 0 if every package_files entry matches.
Checks bytes + sha256 of each file listed in MANIFEST.json against this directory."""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(HERE, "MANIFEST.json"), encoding="utf-8"))

fail = 0
for name, claim in sorted(MAN["package_files"].items()):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        print(f"MISSING  {name}"); fail += 1; continue
    b = open(p, "rb").read()
    ok_b = len(b) == claim["bytes"]
    ok_h = hashlib.sha256(b).hexdigest() == claim["sha256"]
    print(f"{'OK' if ok_b and ok_h else 'FAIL':6s}  {name}  ({len(b)} B)")
    if not (ok_b and ok_h):
        fail += 1
print("RESULT:", "ALL MATCH" if fail == 0 else f"{fail} MISMATCH")
sys.exit(1 if fail else 0)
