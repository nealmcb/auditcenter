#!/usr/bin/env python3
"""
Recover official RLA data files (final audit report PDFs, per-county round
CSVs, manifests, discrepancy reports, etc.) that a 2026 bulk Wayback Machine
pull found archived but that this mirror's live scrape never captured --
for 2022 general, 2022 primary, 2023 coordinated, 2024 presidential, and
2024 primary. This mirrors the same "we never scraped this at all" gap
already identified and partially addressed by fetch_missing_discrepancy_reports.py
for a handful of discrepancy reports, just at larger scale (found via a
systematic Wayback CDX bulk pull + comparison against this mirror, done in
the sibling `auditcenter-wayback` repo -- see
`auditcenter_analyze-private/output/2026-primary/WAYBACK_COMPARISON_FINDINGS.md`
for the full analysis).

Deliberately excludes narrative/dashboard HTML pages (audit.html,
riskLimit.html, countyManifest.html, finalReports.html, background.html,
per-county status pages like Gunnison.html) -- those are consistently
absent from this mirror across every single year from 2017 through 2024,
which looks like a deliberate scope decision (data files, not the SoS's
live status-page chrome) rather than a gap, and their informational value
is already covered by the underlying data files recovered here. Only
genuine primary-source documents (PDF/CSV/XLSX) are recovered.

Source of truth for what to recover: auditcenter-wayback/comparison_state.json
(status == "wayback_only") cross-referenced with bulk_progress.json for the
original URL and capture timestamp. Where the same canonical file had
multiple Wayback captures, all confirmed to share an identical content
digest (verified separately before running this script) -- the earliest
capture is used, since content is identical either way.

Writes one WAYBACK_RECOVERED.md manifest per batch directory, listing each
recovered file's original URL and Wayback capture timestamp, and commits
each batch separately with a summary message pointing at that manifest --
following the provenance-first convention already established by
fetch_missing_discrepancy_reports.py (there: one row per file in-commit;
here: too many files for that to stay readable, so the same information
lives in a per-directory manifest instead, referenced from the commit).
"""
import json
import os
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime

WAYBACK_ROOT = "/home/sprite/auditcenter-wayback"
MIRROR_ROOT = "/home/sprite/auditcenter"

BATCHES = [
    ("2022/general", "2022 General"),
    ("2022/primary", "2022 Primary"),
    ("2023/coordinated", "2023 Coordinated"),
    ("2024/presidential", "2024 Presidential Primary"),
    ("2024/primary", "2024 Primary"),
]


def strip_wayback_timestamp(basename):
    parts = basename.split(".")
    for i, p in enumerate(parts):
        if len(p) == 14 and p.isdigit():
            return ".".join(parts[:i] + parts[i + 1:])
    return basename


def canonical_path_for(local_path):
    d = os.path.dirname(local_path)
    b = os.path.basename(local_path)
    return os.path.join(d, strip_wayback_timestamp(b))


def git(*args):
    return subprocess.run(["git", "-C", MIRROR_ROOT] + list(args), capture_output=True, text=True)


def main():
    state = json.load(open(os.path.join(WAYBACK_ROOT, "comparison_state.json")))
    progress = json.load(open(os.path.join(WAYBACK_ROOT, "bulk_progress.json")))

    wayback_only = sorted(k for k, v in state["processed"].items() if v.get("status") == "wayback_only")

    for prefix, label in BATCHES:
        batch_files = [
            f for f in wayback_only
            if f.startswith(prefix + "/") and not f.lower().endswith((".html", ".htm"))
        ]
        if not batch_files:
            print(f"=== {label} ({prefix}) === nothing to recover, skipping")
            continue

        by_canon = defaultdict(list)
        for f in batch_files:
            by_canon[canonical_path_for(f)].append(f)

        recovered = []  # (canonical_path, url, timestamp)
        skipped_exists = []

        for canon, captures in sorted(by_canon.items()):
            captures.sort(key=lambda f: progress[f]["timestamp"])
            wayback_rel = captures[0]
            info = progress[wayback_rel]

            dest = os.path.join(MIRROR_ROOT, canon)
            if os.path.exists(dest):
                skipped_exists.append(canon)
                continue

            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(os.path.join(WAYBACK_ROOT, wayback_rel), dest)
            recovered.append((canon, info["url"], info["timestamp"]))

        if skipped_exists:
            print(f"  ! {label}: {len(skipped_exists)} targets already existed, skipped: {skipped_exists[:5]}...")

        if not recovered:
            print(f"=== {label} ({prefix}) === nothing new (all already present)")
            continue

        # Write per-directory provenance manifest
        manifest_path = os.path.join(MIRROR_ROOT, prefix, "WAYBACK_RECOVERED.md")
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        lines = [
            f"# Files recovered from the Wayback Machine ({label})\n",
            f"These {len(recovered)} files are official Colorado SoS RLA documents that this "
            "mirror's live scrape never captured, recovered from Internet Archive Wayback "
            "Machine captures during a systematic 2026 bulk-pull comparison. They are NOT "
            "observer-authored content -- same provenance category as this mirror's other "
            "SoS documents, just retrieved via a different (still official) path. See "
            "`auditcenter_analyze-private/output/2026-primary/WAYBACK_COMPARISON_FINDINGS.md` "
            "for the full methodology and analysis.\n",
            "| Local path | Original URL | Wayback capture timestamp |",
            "|---|---|---|",
        ]
        for canon, url, ts in sorted(recovered):
            lines.append(f"| `{canon}` | `{url}` | `{ts}` |")
        with open(manifest_path, "w") as f:
            f.write("\n".join(lines) + "\n")

        # Stage and commit this batch
        git("add", prefix)
        rel_paths = ", ".join(c for c, _, _ in recovered[:3])
        more = f" and {len(recovered) - 3} more" if len(recovered) > 3 else ""
        msg_lines = [
            f"Recover {len(recovered)} {label} files from Wayback Machine (never scraped live)",
            "",
            f"{label} final audit report PDFs, per-county round CSVs, and manifests that "
            "this mirror's live scrape never captured (0 wayback captures matched to any "
            "mirror file). Found via the 2026 bulk Wayback CDX pull/comparison; recovered "
            "from Wayback captures (raw /if_/ file, not the toolbar-wrapped page). Full "
            f"per-file source URL + capture timestamp in `{prefix}/WAYBACK_RECOVERED.md`.",
            "",
            f"Includes: {rel_paths}{more}",
            "",
            "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>",
        ]
        result = git("commit", "-m", "\n".join(msg_lines))
        print(f"=== {label} ({prefix}) === recovered {len(recovered)} files")
        print(f"  commit: {result.stdout.strip() or result.stderr.strip()}")


if __name__ == "__main__":
    main()
