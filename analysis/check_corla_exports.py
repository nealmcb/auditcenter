#!/usr/bin/env python3
"""
check_corla_exports.py — check contestSelection/contestComparison reconciliation
in the nealmcb/auditcenter archive.

Detects two bugs in colorado-rla export SQL:
  Bug 1: contest_selection.sql dumps the full accumulated CVR list across all
         rounds, so the "selected" set is inflated (shows ballots not yet due
         for that round) and per-round files may be identical.
  Bug 2: contest_comparison.sql attributes CVRs to every contest on a ballot
         instead of only the contest they were drawn for.

Usage:
  python3 check_corla_exports.py            # fetch from GitHub and analyse
  python3 check_corla_exports.py --verbose  # also print per-contest detail
"""

import csv
import io
import json
import sys
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

RAW = "https://raw.githubusercontent.com/nealmcb/auditcenter/main"

# Each entry: (label, sel_path, cmp_path)
# cmp_path=None when no corresponding comparison file exists in the archive.
ROUNDS = [
    # 2019 general
    ("2019 general r1", "2019/round_1/contestSelection.csv",        "2019/round_1/contestComparison.csv"),
    ("2019 general r2", "2019/round_2/contestSelection.csv",        "2019/round_2/contestComparison.csv"),
    ("2019 general r3", "2019/round_3/contestSelection.csv",        "2019/round_3/contestComparison.csv"),
    # 2020 general
    ("2020 general r1", "2020/general/round_1/contest_selection.csv", "2020/general/round_1/contestComparison.csv"),
    ("2020 general r2", "2020/general/round_2/contest_selection.csv", "2020/general/round_2/contestComparison.csv"),
    ("2020 general r3", "2020/general/round_3/contest_selection.csv", "2020/general/round_3/contestComparison.csv"),
    # 2020 presidential
    ("2020 presidential r1", "2020/presidential/round_1/contest_selection.csv", "2020/presidential/round_1/contest_comparison.csv"),
    # 2020 state primary (statewide)
    ("2020 statePrimary r1",        "2020/statePrimary/round_1/contest_selection.csv",        "2020/statePrimary/round_1/contestComparison.csv"),
    ("2020 statePrimary r2",        "2020/statePrimary/round_2/contest_selection.csv",        "2020/statePrimary/round_2/contestComparison.csv"),
    # 2020 state primary boulder
    ("2020 statePrimary boulder r1","2020/statePrimary/boulder/round_1/contest_selection.csv","2020/statePrimary/boulder/round_1/contestComparison.csv"),
    ("2020 statePrimary boulder r2","2020/statePrimary/boulder/round_2/contest_selection.csv","2020/statePrimary/boulder/round_2/contestComparison.csv"),
    # 2021 coordinated
    ("2021 coordinated r1", "2021/coordinated/round_1/contest_selection.csv", "2021/coordinated/round_1/contestComparison.csv"),
    ("2021 coordinated r2", "2021/coordinated/round_2/contest_selection.csv", "2021/coordinated/round_2/contestComparison.csv"),
    # 2022 primary
    ("2022 primary r1", "2022/primary/round_1/contest_selection.csv", "2022/primary/round_1/contest_comparison.csv"),
    ("2022 primary r2", "2022/primary/round_2/contest_selection.csv", "2022/primary/round_2/contest_comparison.csv"),
    # 2022 general — no contest-level comparison file in archive
    ("2022 general r1", "2022/general/round_1/contestSelection.csv", None),
    # 2023 coordinated — selection present but no comparison in archive
    ("2023 coordinated r1", "2023/coordinated/round_1/contestSelection.csv", None),
    ("2023 coordinated r2", "2023/coordinated/round_2/contestSelection.csv", None),
    # 2024 general
    ("2024 general r1", "2024/general/round1/contestSelection.csv", "2024/general/round1/contestComparison.csv"),
    ("2024 general r2", "2024/general/round2/contestSelection.csv", "2024/general/round2/contestComparison.csv"),
    ("2024 general r3", "2024/general/round3/contestSelection.csv", "2024/general/round3/contestComparison.csv"),
    # 2024 presidential
    ("2024 presidential r1", "2024/presidential/round_1/contestSelection.csv", "2024/presidential/round_1/contestComparison.csv"),
    ("2024 presidential r2", "2024/presidential/contestSelection.csv",         "2024/presidential/round_2/contestComparisonRound2.csv"),
    # 2024 primary — no comparison file in archive
    ("2024 primary r1", "2024/primary/round1/contestSelection.csv", None),
    # 2025-irv
    ("2025-irv r1", "2025-irv/contest_selection.csv", "2025-irv/contest_comparison.csv"),
    # 2025 coordinated
    ("2025 r1", "2025/round1/contestSelection.csv", "2025/finalReports/contestComparison.csv"),
    ("2025 r2", "2025/round2/contestSelection.csv", "2025/finalReports/contestComparison.csv"),
]

# Rounds grouped by audit for Bug 1 (identical-export) analysis.
# Each group is a list of (label, sel_path) in round order.
AUDIT_GROUPS = [
    [("2019 general r1", "2019/round_1/contestSelection.csv"),
     ("2019 general r2", "2019/round_2/contestSelection.csv"),
     ("2019 general r3", "2019/round_3/contestSelection.csv")],
    [("2020 general r1", "2020/general/round_1/contest_selection.csv"),
     ("2020 general r2", "2020/general/round_2/contest_selection.csv"),
     ("2020 general r3", "2020/general/round_3/contest_selection.csv")],
    [("2020 statePrimary r1", "2020/statePrimary/round_1/contest_selection.csv"),
     ("2020 statePrimary r2", "2020/statePrimary/round_2/contest_selection.csv")],
    [("2020 statePrimary boulder r1", "2020/statePrimary/boulder/round_1/contest_selection.csv"),
     ("2020 statePrimary boulder r2", "2020/statePrimary/boulder/round_2/contest_selection.csv")],
    [("2021 coordinated r1", "2021/coordinated/round_1/contest_selection.csv"),
     ("2021 coordinated r2", "2021/coordinated/round_2/contest_selection.csv")],
    [("2022 primary r1", "2022/primary/round_1/contest_selection.csv"),
     ("2022 primary r2", "2022/primary/round_2/contest_selection.csv")],
    [("2023 coordinated r1", "2023/coordinated/round_1/contestSelection.csv"),
     ("2023 coordinated r2", "2023/coordinated/round_2/contestSelection.csv")],
    [("2024 general r1", "2024/general/round1/contestSelection.csv"),
     ("2024 general r2", "2024/general/round2/contestSelection.csv"),
     ("2024 general r3", "2024/general/round3/contestSelection.csv")],
    [("2025 r1", "2025/round1/contestSelection.csv"),
     ("2025 r2", "2025/round2/contestSelection.csv")],
]


def fetch_text(path: str) -> Optional[str]:
    url = f"{RAW}/{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "check-corla-exports/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [fetch error] {path}: {e}", file=sys.stderr)
        return None


def parse_selection(text: str) -> dict[str, set[int]]:
    """Returns {contest_name: set(cvr_ids)}."""
    result: dict[str, set[int]] = {}
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        name = row.get("contest_name", "").strip()
        raw = row.get("contest_cvr_ids", "[]").strip()
        if not raw or raw == "[]":
            result.setdefault(name, set())
            continue
        try:
            ids = json.loads(raw)
            result[name] = set(int(x) for x in ids)
        except Exception:
            result.setdefault(name, set())
    return result


def parse_comparison(text: str) -> dict[str, set[int]]:
    """Returns {contest_name: set(cvr_ids with non-null timestamp)} — genuine comparisons only."""
    result: dict[str, set[int]] = {}
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        ts = row.get("timestamp", "").strip()
        if not ts:
            continue  # placeholder row — not yet audited
        name = row.get("contest_name", "").strip()
        raw_id = row.get("cvr_id", "").strip()
        if not raw_id:
            continue
        try:
            cvr_id = int(raw_id)
        except ValueError:
            continue
        result.setdefault(name, set()).add(cvr_id)
    return result


@dataclass
class RoundResult:
    label: str
    sel_contests: int = 0
    cmp_contests: int = 0
    total_sel_ids: int = 0
    total_cmp_ids: int = 0
    affected_contests: int = 0   # contests with sel_only > 0 or cmp_only > 0
    sel_only_total: int = 0      # Bug 1 proxy: selected but not compared
    cmp_only_total: int = 0      # Bug 2 proxy: compared but not selected
    no_cmp_file: bool = False
    per_contest: list = field(default_factory=list)  # (name, sel, cmp, sel_only, cmp_only)


def analyse_round(label: str, sel_path: str, cmp_path: Optional[str], verbose: bool) -> RoundResult:
    result = RoundResult(label=label)
    print(f"  Fetching selection: {sel_path}", file=sys.stderr)
    sel_text = fetch_text(sel_path)
    if sel_text is None:
        return result
    sel = parse_selection(sel_text)
    result.sel_contests = len(sel)
    result.total_sel_ids = sum(len(v) for v in sel.values())

    if cmp_path is None:
        result.no_cmp_file = True
        return result

    print(f"  Fetching comparison: {cmp_path}", file=sys.stderr)
    cmp_text = fetch_text(cmp_path)
    if cmp_text is None:
        result.no_cmp_file = True
        return result
    cmp = parse_comparison(cmp_text)
    result.cmp_contests = len(cmp)
    result.total_cmp_ids = sum(len(v) for v in cmp.values())

    # Per-contest analysis: all contest names seen in either file
    all_contests = set(sel.keys()) | set(cmp.keys())
    for name in sorted(all_contests):
        s_ids = sel.get(name, set())
        c_ids = cmp.get(name, set())
        sel_only = len(s_ids - c_ids)
        cmp_only = len(c_ids - s_ids)
        result.per_contest.append((name, len(s_ids), len(c_ids), sel_only, cmp_only))
        if sel_only > 0 or cmp_only > 0:
            result.affected_contests += 1
        result.sel_only_total += sel_only
        result.cmp_only_total += cmp_only

    return result


def analyse_bug1_identical(groups: list, verbose: bool) -> list[tuple]:
    """
    For each multi-round audit, compare selection sets across rounds.
    Returns list of (audit_label, round_labels, identical_pairs, subset_pairs, note).
    """
    findings = []
    for group in groups:
        if len(group) < 2:
            continue
        audit_label = group[0][0].rsplit(" r", 1)[0]
        print(f"  Bug1 check: {audit_label}", file=sys.stderr)
        round_sels = []
        for label, path in group:
            text = fetch_text(path)
            if text is None:
                round_sels.append((label, None))
                continue
            round_sels.append((label, parse_selection(text)))

        pairs = []
        for i in range(len(round_sels) - 1):
            l1, s1 = round_sels[i]
            l2, s2 = round_sels[i + 1]
            if s1 is None or s2 is None:
                continue
            # Compare all contests' ID sets
            all_names = set(s1.keys()) | set(s2.keys())
            identical_contests = sum(1 for n in all_names if s1.get(n, set()) == s2.get(n, set()))
            subset_contests = sum(1 for n in all_names if s1.get(n, set()) < s2.get(n, set()))
            grown_contests = sum(1 for n in all_names if len(s2.get(n, set())) > len(s1.get(n, set())))
            pairs.append((l1, l2, identical_contests, len(all_names), grown_contests))
        findings.append((audit_label, pairs))
    return findings


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print("=" * 72)
    print("Colorado RLA export reconciliation checker")
    print("Bugs: (1) selection accumulates all rounds; (2) comparison cross-attributes contests")
    print("=" * 72)
    print()

    # ── Bug 2 / reconciliation analysis (per round) ──────────────────────────
    print("## Per-round reconciliation (Bug 1 proxy: sel_only; Bug 2 proxy: cmp_only)")
    print()
    print(f"{'Round':<28} {'sel_c':>5} {'cmp_c':>5} {'sel_ids':>8} {'cmp_ids':>8} {'aff_c':>6} {'sel_only':>9} {'cmp_only':>9}  note")
    print("-" * 105)

    all_results = []
    for label, sel_path, cmp_path in ROUNDS:
        print(f"Analysing: {label}", file=sys.stderr)
        r = analyse_round(label, sel_path, cmp_path, verbose)
        all_results.append(r)

        note = "no cmp file" if r.no_cmp_file else ""
        print(f"{r.label:<28} {r.sel_contests:>5} {r.cmp_contests:>5} {r.total_sel_ids:>8} {r.total_cmp_ids:>8} {r.affected_contests:>6} {r.sel_only_total:>9} {r.cmp_only_total:>9}  {note}")

        if verbose and r.per_contest:
            print(f"  {'contest':<60} {'sel':>6} {'cmp':>6} {'sel_only':>9} {'cmp_only':>9}")
            for name, s, c, so, co in r.per_contest:
                if so > 0 or co > 0:
                    print(f"  {name:<60} {s:>6} {c:>6} {so:>9} {co:>9}")

    # Summary
    rounds_with_cmp = [r for r in all_results if not r.no_cmp_file]
    affected = [r for r in rounds_with_cmp if r.sel_only_total > 0 or r.cmp_only_total > 0]
    sel_only_rounds = [r for r in rounds_with_cmp if r.sel_only_total > 0]
    cmp_only_rounds = [r for r in rounds_with_cmp if r.cmp_only_total > 0]

    print()
    print(f"Rounds with comparison file:  {len(rounds_with_cmp)}")
    print(f"Rounds with any discrepancy:  {len(affected)}/{len(rounds_with_cmp)}")
    print(f"Rounds with sel_only > 0:     {len(sel_only_rounds)}/{len(rounds_with_cmp)}  (Bug 1 indicator)")
    print(f"Rounds with cmp_only > 0:     {len(cmp_only_rounds)}/{len(rounds_with_cmp)}  (Bug 2 indicator)")
    print(f"Total sel_only across all:    {sum(r.sel_only_total for r in rounds_with_cmp)}")
    print(f"Total cmp_only across all:    {sum(r.cmp_only_total for r in rounds_with_cmp)}")
    print(f"Total affected contest-rounds:{sum(r.affected_contests for r in rounds_with_cmp)}")
    print()

    # ── Bug 1 / identical-round analysis ────────────────────────────────────
    print("## Bug 1 — per-round selection file comparison (identical sets = same accumulated list exported)")
    print()
    print("Files should differ across rounds: round N+1 should draw NEW ballots, so its list should grow.")
    print("If selections are identical across rounds, Bug 1 may be causing stale/unchanging exports.")
    print()

    bug1_findings = analyse_bug1_identical(AUDIT_GROUPS, verbose)
    for audit_label, pairs in bug1_findings:
        print(f"  {audit_label}")
        for l1, l2, identical, total, grown in pairs:
            pct_identical = 100.0 * identical / total if total else 0
            flags = []
            if identical == total:
                flags.append("ALL IDENTICAL — classic Bug 1 signature")
            elif pct_identical > 50:
                flags.append(f"{pct_identical:.0f}% identical contests — likely Bug 1")
            if grown > 0:
                flags.append(f"{grown}/{total} contests gained new IDs in round 2")
            flag_str = "; ".join(flags) if flags else "selections differ (expected)"
            print(f"    {l1} vs {l2}: {identical}/{total} contests identical — {flag_str}")
        print()

    print("Done.")


if __name__ == "__main__":
    main()
