#!/usr/bin/env python3
"""verify_manifest.py v3 — full-coverage package verifier (VIXOR TASK 23 edition).

Upgrades over v2 (owner directive, 12 requirements):
  1. Checks size AND sha256 of every registered file against real bytes.
  2. Compares the ACTUAL on-disk inventory with the manifest inventory.
  3. Rejects missing files AND unregistered extra files unless explicitly excluded.
  4. Rejects traversal paths ('..', absolute, drive letters, backslashes).
  5. Handles symlinks safely: no escaping the package root; dangling/outside links fail.
  6. Validates JSON structure, mandatory fields and data types (duplicate JSON keys rejected).
  7. Rejects duplicate/conflicting paths across sections (exact and case-insensitive).
  8. Logs explicit exclusions per file with reason and scope.
  9. Treats MANIFEST.json itself transparently: excluded by design, structurally
     validated, never claims a self-hash it cannot have.
 10. The historical MANIFEST (v1) is REGISTERED as a normal entry => its hash is
     re-verifiable from current files (not merely a historical claim).
 11. 'PASS' requires FULL coverage: every file physically on disk must be registered,
     excluded, or the manifest itself — no blanket ALL MATCH over a subset.
 12. Non-zero exit code on ANY failure (0 = pass, 1 = verification failure, 2 = usage).

Usage:
    python3 verify_manifest.py [package_root] [--manifest PATH]
Default root: directory containing this script. Default manifest: <root>/MANIFEST.json
"""
import hashlib
import json
import os
import posixpath
import re
import sys

MANIFEST_NAME = "MANIFEST.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")

failures = []
warnings = []


def fail(msg):
    failures.append(msg)
    print(f"FAIL    {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"WARN    {msg}")


class DuplicateKeyError(ValueError):
    pass


def _pairs_hook(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise DuplicateKeyError(f"duplicate JSON key: {k!r}")
        seen.add(k)
    return dict(pairs)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_within(root_real, candidate_real):
    return candidate_real == root_real or candidate_real.startswith(root_real + os.sep)


def validate_path_safety(p):
    """Return error string or None. p is a manifest-registered relative POSIX path."""
    if not isinstance(p, str) or not p:
        return "path must be a non-empty string"
    if "\\" in p:
        return "backslash in path (not POSIX)"
    if p.startswith("/") or (len(p) > 1 and p[1] == ":"):
        return "absolute path not allowed"
    if posixpath.normpath(p) != p:
        return f"path not normalized (normpath={posixpath.normpath(p)!r})"
    parts = p.split("/")
    if any(part == ".." for part in parts):
        return "traversal '..' component not allowed"
    if any(part == "" for part in parts):
        return "empty path component"
    return None


def validate_entry(name, section, e):
    errs = []
    if not isinstance(e, dict):
        return [f"{section}/{name}: entry must be an object, got {type(e).__name__}"]
    allowed = {"bytes", "sha256", "note"}
    for k in e:
        if k not in allowed:
            errs.append(f"{section}/{name}: unknown field {k!r} (allowed: {sorted(allowed)})")
    b = e.get("bytes")
    if isinstance(b, bool) or not isinstance(b, int) or b < 0:
        errs.append(f"{section}/{name}: 'bytes' must be a non-negative integer, got {b!r}")
    s = e.get("sha256")
    if not isinstance(s, str) or not HEX64.match(s):
        errs.append(f"{section}/{name}: 'sha256' must be 64-char lowercase hex, got {s!r}")
    n = e.get("note")
    if n is not None and not isinstance(n, str):
        errs.append(f"{section}/{name}: 'note' must be a string when present")
    return errs


def validate_exclusion(name, e):
    errs = []
    if not isinstance(e, dict):
        return [f"exclusions/{name}: exclusion must be an object"]
    for req in ("reason", "scope"):
        v = e.get(req)
        if not isinstance(v, str) or not v.strip():
            errs.append(f"exclusions/{name}: '{req}' must be a non-empty string")
    for opt in ("added_by_task",):
        v = e.get(opt)
        if v is not None and not isinstance(v, str):
            errs.append(f"exclusions/{name}: '{opt}' must be a string when present")
    allowed = {"reason", "scope", "added_by_task"}
    for k in e:
        if k not in allowed:
            errs.append(f"exclusions/{name}: unknown field {k!r}")
    return errs


def main():
    args = sys.argv[1:]
    root = None
    manifest_path = None
    i = 0
    while i < len(args):
        if args[i] == "--manifest":
            if i + 1 >= len(args):
                print("USAGE ERROR: --manifest requires a value")
                return 2
            manifest_path = args[i + 1]
            i += 2
        elif args[i].startswith("--"):
            print(f"USAGE ERROR: unknown option {args[i]}")
            return 2
        else:
            root = args[i]
            i += 1
    if root is None:
        root = os.path.dirname(os.path.abspath(__file__))
    if manifest_path is None:
        manifest_path = os.path.join(root, MANIFEST_NAME)
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"USAGE ERROR: package root not found: {root}")
        return 2
    root_real = os.path.realpath(root)

    print(f"verify_manifest.py v3 — root={root}")
    print(f"manifest={manifest_path}")

    # ---- load + duplicate-key check (req 6, 7) ----
    try:
        raw = open(manifest_path, "rb").read()
    except OSError as e:
        print(f"FATAL   manifest unreadable: {e}")
        return 1
    try:
        man = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs_hook)
    except DuplicateKeyError as e:
        print(f"FATAL   {e} (duplicate keys make section-conflict checks unreliable)")
        return 1
    except Exception as e:
        print(f"FATAL   MANIFEST unparseable as UTF-8 JSON: {e}")
        return 1
    if not isinstance(man, dict):
        print("FATAL   MANIFEST must be a JSON object")
        return 1
    manifest_bytes = len(raw)

    # ---- schema validation (req 6) ----
    schema_ok = True
    for req, typ in (("package", str), ("manifest_version", int), ("generated_at", str),
                     ("files", dict), ("evidence", dict), ("exclusions", dict)):
        v = man.get(req)
        if isinstance(v, bool) or not isinstance(v, typ):
            fail(f"schema: top-level '{req}' must be {typ.__name__}, got {type(v).__name__}")
            schema_ok = False
    if not schema_ok:
        print("RESULT: FAIL — manifest schema invalid; content checks skipped")
        return 1
    known_top = {"package", "manifest_version", "generated_at", "generated_by_task",
                 "supersedes", "historical_manifest_v1", "language", "verdict",
                 "files", "evidence", "exclusions", "secret_scan", "manifest_self_note",
                 "coverage_contract", "verifier", "pr10_head_verified", "pr10_merged",
                 "notes"}
    for k in man:
        if k not in known_top:
            warn(f"unknown top-level key {k!r} (allowed-forward-compat)")

    files_sec = man["files"]
    evid_sec = man["evidence"]
    excl_sec = man["exclusions"]

    entry_errs = []
    for section in ("files", "evidence"):
        for name, e in man[section].items():
            entry_errs += validate_entry(name, section, e)
    for name, e in excl_sec.items():
        entry_errs += validate_exclusion(name, e)
    for msg in entry_errs:
        fail("schema: " + msg)
    if entry_errs:
        print("RESULT: FAIL — manifest entry schema invalid; content checks skipped")
        return 1

    # ---- path-safety validation of every registered/excluded path (req 4, 5) ----
    path_err = False
    for section in ("files", "evidence"):
        for name in man[section]:
            err = validate_path_safety(name)
            if err:
                fail(f"path-safety {section}/{name}: {err}")
                path_err = True
            if name == MANIFEST_NAME:
                fail(f"path-conflict {section}/{MANIFEST_NAME}: the manifest cannot register itself (no self-hash possible)")
                path_err = True
    for name in excl_sec:
        err = validate_path_safety(name)
        if err:
            fail(f"path-safety exclusions/{name}: {err}")
            path_err = True
    if path_err:
        print("RESULT: FAIL — unsafe paths present; refusing to continue")
        return 1

    # ---- duplicate/conflict detection (req 7) ----
    all_paths = list(files_sec) + list(evid_sec) + list(excl_sec)
    dup_exact = {p for p in all_paths if all_paths.count(p) > 1}
    for p in sorted(dup_exact):
        fail(f"conflict: path {p!r} appears in more than one section")
    lower_map = {}
    for p in all_paths:
        lower_map.setdefault(p.lower(), set()).add(p)
    for low, variants in sorted(lower_map.items()):
        if len(variants) > 1:
            fail(f"conflict: case-insensitive collision {sorted(variants)} "
                 "(breaks on case-insensitive filesystems/extractions)")

    # ---- MANIFEST self-handling (req 9) ----
    if MANIFEST_NAME not in excl_sec:
        fail(f"{MANIFEST_NAME} must be listed in 'exclusions' with an explicit self-reference reason")
    else:
        print(f"OK      {MANIFEST_NAME}: self-excluded by design "
              f"({manifest_bytes} B, not self-hashed — structural validation only)")

    # ---- inventory walk (req 2, 5) ----
    actual_files = []   # regular files (not symlinks)
    actual_links = []   # symlinks (file or dir), recorded for policy checks
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        for dn in list(dirnames):
            full = os.path.join(dirpath, dn)
            if os.path.islink(full):
                actual_links.append(os.path.relpath(full, root).replace(os.sep, "/"))
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if os.path.islink(full):
                actual_links.append(rel)
            elif os.path.isfile(full):
                actual_files.append(rel)
    actual_set = set(actual_files)

    registered = {**files_sec, **evid_sec}
    if dup_exact or any(len(v) > 1 for v in lower_map.values()):
        print("RESULT: FAIL — section conflicts present; refusing content verification")
        return 1

    # missing (registered but not on disk)
    missing = sorted(set(registered) - actual_set)
    for p in missing:
        fail(f"MISSING {p} (registered in manifest, absent on disk)")

    # unregistered extras (on disk but neither registered nor excluded nor manifest)
    unregistered = sorted(actual_set - set(registered) - set(excl_sec) - {MANIFEST_NAME})
    for p in unregistered:
        fail(f"UNREGISTERED {p} (on disk, not in files/evidence, not excluded)")

    # symlink policy (req 5)
    for rel in sorted(actual_links):
        full_real = os.path.realpath(os.path.join(root, rel))
        if not os.path.exists(os.path.realpath(os.path.join(root, rel))):
            fail(f"SYMLINK {rel}: dangling (target does not exist)")
            continue
        if not is_within(root_real, full_real):
            fail(f"SYMLINK {rel}: escapes package root -> {full_real}")
            continue
        if os.path.isdir(full_real):
            fail(f"SYMLINK {rel}: directory symlink inside root — directories are not hashable package content")
            continue
        if rel in registered:
            print(f"NOTE    SYMLINK {rel}: inside root, registered — content of target will be hashed")
        else:
            fail(f"SYMLINK {rel}: inside root but not registered/excluded")

    # content verification of registered files (req 1)
    ok_count = 0
    for section in ("files", "evidence"):
        for name, meta in sorted(man[section].items()):
            local = os.path.join(root, name)
            if name in missing or not os.path.isfile(local):
                continue  # already failed as missing / symlink handled
            size = os.path.getsize(local)
            digest = sha256_of(local)
            if size == meta["bytes"] and digest == meta["sha256"]:
                ok_count += 1
                note = f" — {meta['note']}" if meta.get("note") else ""
                print(f"OK      {name}  ({size} B{note})")
            else:
                fail(f"{name}: size/hash mismatch (disk {size} B/{digest[:12]}… vs manifest "
                     f"{meta['bytes']} B/{meta['sha256'][:12]}…)")

    # exclusions accounting (req 8)
    excluded_on_disk = 0
    for name, meta in sorted(excl_sec.items()):
        if name == MANIFEST_NAME:
            continue  # already reported in self-handling
        if name in actual_set:
            excluded_on_disk += 1
            print(f"EXCLUDED {name}  (on disk — reason: {meta.get('reason')}; scope: {meta.get('scope')})")
        else:
            print(f"EXCLUDED {name}  (not present — reservation; reason: {meta.get('reason')})")

    # ---- coverage summary (req 11) — no blanket ALL MATCH without full coverage ----
    total_disk = len(actual_files) + len(actual_links)
    accounted = len(actual_set & set(registered)) + excluded_on_disk + (1 if MANIFEST_NAME in actual_set else 0)
    n_fail = len(failures)
    print("-" * 78)
    print(f"COVERAGE: files on disk = {total_disk} (regular {len(actual_files)} + symlinks {len(actual_links)})")
    print(f"          registered checked OK = {ok_count} | registered FAIL/missing = "
          f"{len(registered) - ok_count} | unregistered = {len(unregistered)} | "
          f"excluded on disk = {excluded_on_disk} (+1 manifest self)")
    print(f"          accounted = {accounted}/{total_disk} regular+manifest")
    if n_fail == 0 and not missing and not unregistered:
        print(f"RESULT: PASS — full coverage proven ({ok_count} registered entries verified, "
              f"{excluded_on_disk + 1} explicitly excluded, 0 unregistered, 0 missing)")
        return 0
    print(f"RESULT: FAIL — {n_fail} failure(s); coverage NOT complete")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:  # unexpected internal error must also be non-zero (req 12)
        print(f"FATAL   internal error: {type(e).__name__}: {e}")
        sys.exit(2)
