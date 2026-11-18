#!/usr/bin/env python3
"""Run every script under scripts/<group>/ that has an expected output, and compare.

Usage: python3 verification/run_scripts.py [group ...]
Groups: curve, edges, symbolic, symbolic-referee, trinity, continuity (default: all).

The output of each script must equal expected/<group>/<name>.out byte for byte. The group continuity
belongs to the second paper (continuity/paper/) and lives in continuity/scripts/ and continuity/expected/.
Every script uses exact rationals, fixed precision and fixed random seeds, so the
output is deterministic. A difference fails the check. The expected files are not
rewritten by this script.
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS = ["curve", "edges", "symbolic", "symbolic-referee", "trinity", "continuity"]


def dirs(g):
    if g == "continuity":
        return os.path.join(ROOT, "continuity", "expected"), os.path.join(ROOT, "continuity", "scripts")
    return os.path.join(ROOT, "expected", g), os.path.join(ROOT, "scripts", g)


def main(argv):
    groups = argv or GROUPS
    failed = []
    ran = 0
    for g in groups:
        exp_dir, scr_dir = dirs(g)
        names = sorted(f[:-4] for f in os.listdir(exp_dir) if f.endswith(".out"))
        for name in names:
            script = os.path.join(scr_dir, name + ".py")
            if not os.path.exists(script):
                failed.append(f"{g}/{name}: expected output without a script")
                continue
            t0 = time.time()
            res = subprocess.run([sys.executable, name + ".py"], cwd=scr_dir,
                                 capture_output=True, text=True)
            with open(os.path.join(exp_dir, name + ".out"), encoding="utf-8") as fh:
                want = fh.read()
            got = res.stdout + res.stderr
            ok = res.returncode == 0 and got == want
            ran += 1
            print(f"{'ok  ' if ok else 'FAIL'} {g}/{name} ({time.time() - t0:.0f}s)", flush=True)
            if not ok:
                failed.append(f"{g}/{name}: rc={res.returncode}")
                for i, (a, b) in enumerate(zip(want.splitlines(), got.splitlines())):
                    if a != b:
                        print(f"  first difference at line {i + 1}:\n  want: {a}\n  got:  {b}")
                        break
                else:
                    print(f"  line counts differ: want {len(want.splitlines())}, got {len(got.splitlines())}")
    print(f"{ran} scripts run, {len(failed)} failed")
    for f in failed:
        print("  " + f)
    return 1 if failed or ran == 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
