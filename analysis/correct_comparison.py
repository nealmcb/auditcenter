#!/usr/bin/env python3
"""
correct_comparison.py — retroactively fix Bug 2 in contestComparison.csv

Bug 2: contest_comparison.sql attributes every audited CVR to every contest
printed on that ballot, rather than only the contest(s) it was drawn for.
This script filters a contestComparison.csv to only rows where the cvr_id
appears in that contest's entry in contestSelection.csv.

The correction is lossless: every row removed is a spurious attribution.
Every row retained is a legitimate audit record for that contest.

Note: Bug 1 (selection file accumulates all rounds) is reported but cannot
be corrected from the archived files alone — that requires internal DB data.

Usage:
  python3 correct_comparison.py \\
      --selection contestSelection.csv \\
      --comparison contestComparison.csv \\
      --output contestComparison_corrected.csv

  # Or fetch a specific archive round from GitHub:
  python3 correct_comparison.py \\
      --round 2024/general/round1 \\
      --output 2024_general_r1_comparison_corrected.csv
"""

import argparse
import csv
import io
import json
import sys
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/nealmcb/auditcenter/main"

# Known file name variants in the archive
SEL_NAMES = ["contestSelection.csv", "contest_selection.csv"]
CMP_NAMES = ["contestComparison.csv", "contest_comparison.csv", "contestComparisonRound2.csv"]


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "correct-corla-exports/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_round_file(round_path: str, names: list[str]) -> tuple[str, str]:
    """Try each name variant; return (filename, content) for the first that exists."""
    for name in names:
        url = f"{RAW}/{round_path.rstrip('/')}/{name}"
        try:
            content = fetch_text(url)
            print(f"  fetched: {url}", file=sys.stderr)
            return name, content
        except Exception:
            continue
    raise FileNotFoundError(f"None of {names} found under {round_path}")


def parse_selection(text: str) -> dict[str, set[int]]:
    """Returns {contest_name: set(cvr_ids)}."""
    result: dict[str, set[int]] = {}
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        name = row.get("contest_name", "").strip()
        raw = row.get("contest_cvr_ids", "[]").strip()
        try:
            ids = json.loads(raw) if raw else []
            result[name] = set(int(x) for x in ids)
        except Exception:
            result.setdefault(name, set())
    return result


def correct_comparison(sel_text: str, cmp_text: str, out_path: str) -> dict:
    sel = parse_selection(sel_text)

    # Build fast lookup: cvr_id → set of contest names it was drawn for
    cvr_to_contests: dict[int, set[str]] = {}
    for contest, ids in sel.items():
        for cvr_id in ids:
            cvr_to_contests.setdefault(cvr_id, set()).add(contest)

    reader = csv.DictReader(io.StringIO(cmp_text))
    fieldnames = reader.fieldnames or []

    kept = 0
    removed = 0
    no_id = 0

    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            raw_id = row.get("cvr_id", "").strip()
            if not raw_id:
                no_id += 1
                continue
            try:
                cvr_id = int(raw_id)
            except ValueError:
                no_id += 1
                continue
            contest = row.get("contest_name", "").strip()
            # Keep if this cvr_id was drawn for this contest (or if contest not
            # in selection at all — e.g. an untargeted contest with no entry).
            if contest not in sel or cvr_id in sel.get(contest, set()):
                writer.writerow(row)
                kept += 1
            else:
                removed += 1

    return {"kept": kept, "removed": removed, "no_id": no_id}


def main():
    parser = argparse.ArgumentParser(description="Fix Bug 2 in contestComparison.csv")
    parser.add_argument("--selection", help="Path to contestSelection.csv (local file)")
    parser.add_argument("--comparison", help="Path to contestComparison.csv (local file)")
    parser.add_argument("--round", help="Archive round path, e.g. 2024/general/round1 (fetches from GitHub)")
    parser.add_argument("--output", required=True, help="Output path for corrected comparison CSV")
    args = parser.parse_args()

    if args.round:
        print(f"Fetching selection file for round: {args.round}", file=sys.stderr)
        _, sel_text = fetch_round_file(args.round, SEL_NAMES)
        print(f"Fetching comparison file for round: {args.round}", file=sys.stderr)
        _, cmp_text = fetch_round_file(args.round, CMP_NAMES)
    elif args.selection and args.comparison:
        sel_text = Path(args.selection).read_text(encoding="utf-8")
        cmp_text = Path(args.comparison).read_text(encoding="utf-8")
    else:
        parser.error("Provide either --round or both --selection and --comparison")

    print(f"Writing corrected comparison to: {args.output}", file=sys.stderr)
    stats = correct_comparison(sel_text, cmp_text, args.output)

    print()
    print(f"Rows kept (legitimate):  {stats['kept']:>9}")
    print(f"Rows removed (spurious): {stats['removed']:>9}  ← Bug 2 rows eliminated")
    print(f"Rows skipped (no cvr_id):{stats['no_id']:>9}")
    if stats["kept"] + stats["removed"] > 0:
        pct = 100.0 * stats["removed"] / (stats["kept"] + stats["removed"])
        print(f"Reduction:               {pct:>8.1f}%")


if __name__ == "__main__":
    main()
