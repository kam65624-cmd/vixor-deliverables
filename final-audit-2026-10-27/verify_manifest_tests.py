#!/usr/bin/env python3
"""verify_manifest_tests.py — independent positive/negative test suite for
verify_manifest.py v3 (TASK 23).

Every test copies the REAL package (real bytes, no mocks) into a fresh temp dir,
mutates it in a specific way, runs the REAL verifier via subprocess, and checks
the exit code (and, where relevant, the output markers).

Scenarios:
  T1  intact package                        -> exit 0 (PASS)
  T2  registered file deleted               -> exit 1
  T3  registered file byte-modified         -> exit 1
  T4  extra unregistered file added         -> exit 1
  T5  forged sha256 inside MANIFEST         -> exit 1
  T6  traversal path ('../') in MANIFEST    -> exit 1
  T7  symlink escaping the package root     -> exit 1
  T8  wrong field types inside MANIFEST     -> exit 1
  T9  file added + documented exclusion     -> exit 0 (with EXCLUDED marker)
  T10 duplicate path across sections        -> exit 1

Exit code: 0 iff ALL tests pass. Runs on the package this file lives in.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFIER = os.path.join(HERE, "verify_manifest.py")
MANIFEST = "MANIFEST.json"
PROBE_FILE = "evidence/test-evidence-r22_run1_2026-10-27.log"
FAKE_SHA = "b" * 64
ALT_SHA = "a" * 64


def fresh_copy(base, name):
    dst = os.path.join(base, name)
    shutil.copytree(HERE, dst, symlinks=True)
    return dst


def run_verifier(root):
    r = subprocess.run([sys.executable, VERIFIER, root],
                       capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout + r.stderr


def load_manifest(root):
    with open(os.path.join(root, MANIFEST), encoding="utf-8") as f:
        return json.load(f)


def save_manifest(root, man):
    with open(os.path.join(root, MANIFEST), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1, ensure_ascii=False)


def t1_intact(base):
    root = fresh_copy(base, "t1")
    return run_verifier(root)


def t2_missing(base):
    root = fresh_copy(base, "t2")
    os.remove(os.path.join(root, PROBE_FILE))
    return run_verifier(root)


def t3_modified(base):
    root = fresh_copy(base, "t3")
    p = os.path.join(root, "H1H2_ASSESSMENT.md")
    with open(p, "ab") as f:
        f.write(b"X")  # single byte flip by append — real byte modification
    return run_verifier(root)


def t4_extra(base):
    root = fresh_copy(base, "t4")
    with open(os.path.join(root, "STOWAWAY.txt"), "wb") as f:
        f.write(b"unregistered stowaway")
    return run_verifier(root)


def t5_forged_sha(base):
    root = fresh_copy(base, "t5")
    man = load_manifest(root)
    victim = "EXECUTIVE_SUMMARY_AR.md"
    man["files"][victim]["sha256"] = FAKE_SHA  # valid hex, wrong value
    save_manifest(root, man)
    return run_verifier(root)


def t6_traversal(base):
    root = fresh_copy(base, "t6")
    man = load_manifest(root)
    man["files"]["../outside.txt"] = {"bytes": 1, "sha256": FAKE_SHA}
    save_manifest(root, man)
    return run_verifier(root)


def t7_symlink_escape(base):
    root = fresh_copy(base, "t7")
    p = os.path.join(root, PROBE_FILE)
    os.remove(p)
    os.symlink("/etc/hostname", p)  # outside the package root
    return run_verifier(root)


def t8_bad_types(base):
    root = fresh_copy(base, "t8")
    man = load_manifest(root)
    man["files"]["ALERT_STATUS.md"]["bytes"] = "8647"  # string instead of int
    save_manifest(root, man)
    return run_verifier(root)


def t9_documented_exclusion(base):
    root = fresh_copy(base, "t9")
    with open(os.path.join(root, "NOTE_EXTRA.txt"), "wb") as f:
        f.write("owner-requested supplementary note".encode())
    man = load_manifest(root)
    man["exclusions"]["NOTE_EXTRA.txt"] = {
        "reason": "supplementary owner note added after freeze (TEST T9 scenario)",
        "scope": "single file, this test only",
        "added_by_task": "TASK 23 tests",
    }
    save_manifest(root, man)
    code, out = run_verifier(root)
    ok_marker = "EXCLUDED NOTE_EXTRA.txt" in out
    return (0 if (code == 0 and ok_marker) else 1), out


def t10_duplicate_sections(base):
    root = fresh_copy(base, "t10")
    man = load_manifest(root)
    man["evidence"]["ALERT_STATUS.md"] = dict(man["files"]["ALERT_STATUS.md"])
    save_manifest(root, man)
    return run_verifier(root)


TESTS = [
    ("T1  intact package -> PASS", t1_intact, 0),
    ("T2  registered file missing -> FAIL", t2_missing, 1),
    ("T3  registered file byte-modified -> FAIL", t3_modified, 1),
    ("T4  extra unregistered file -> FAIL", t4_extra, 1),
    ("T5  forged sha256 in manifest -> FAIL", t5_forged_sha, 1),
    ("T6  traversal path in manifest -> FAIL", t6_traversal, 1),
    ("T7  symlink escaping root -> FAIL", t7_symlink_escape, 1),
    ("T8  wrong field types -> FAIL", t8_bad_types, 1),
    ("T9  documented exclusion -> PASS", t9_documented_exclusion, 0),
    ("T10 duplicate path across sections -> FAIL", t10_duplicate_sections, 1),
]


def main():
    if not os.path.isfile(VERIFIER):
        print(f"FATAL verifier not found: {VERIFIER}")
        return 2
    base = tempfile.mkdtemp(prefix="vmp3_tests_")
    print(f"verify_manifest_tests.py — real-package copies under {base}")
    print(f"verifier: {VERIFIER}")
    print("-" * 78)
    results = []
    all_out = []
    for name, fn, expected in TESTS:
        try:
            code, out = fn(base)
        except Exception as e:
            code, out = -1, f"exception: {type(e).__name__}: {e}"
        verdict = "PASS" if code == expected else "FAIL"
        results.append((name, expected, code, verdict))
        last = [l for l in out.splitlines() if l.startswith("RESULT:")]
        summary = last[-1] if last else out.strip().splitlines()[-1] if out.strip() else "(no output)"
        print(f"{verdict}  {name}  (expected exit {expected}, got {code})")
        print(f"     └─ {summary}")
        all_out.append(f"\n===== {name} (expected {expected}, got {code}, {verdict}) =====\n{out}")
    print("-" * 78)
    failed = [r for r in results if r[3] != "PASS"]
    print(f"SUITE RESULT: {'ALL 10 TESTS PASS' if not failed else f'{len(failed)} TEST(S) FAILED'}")
    # keep full transcripts for the evidence log
    log = os.path.join(tempfile.gettempdir(), "vmp3_tests_full_output.txt")
    with open(log, "w", encoding="utf-8") as f:
        f.write("".join(all_out))
    print(f"full transcripts: {log}")
    shutil.rmtree(base, ignore_errors=True)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
