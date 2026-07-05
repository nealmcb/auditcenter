# Analysis: contestSelection / contestComparison reconciliation bugs

This directory contains tools and findings from an investigation into two SQL
bugs in the ColoradoRLA export layer that cause `contestSelection.csv` and
`contestComparison.csv` to not reconcile.

## Background

Colorado's Audit Center publishes per-round export files for each audit.
Two of those files — `contestSelection.csv` (the CVR IDs drawn by the SHA-256
PRNG for each contest) and `contestComparison.csv` (the CVR-level comparisons
submitted by audit boards) — should reconcile: every selected CVR ID should
eventually get a comparison record, and every comparison record should trace
back to a selection.

They don't, due to two independent bugs in the server SQL:

**Bug 1 — `contest_selection.sql` has no round filter.**
`ComparisonAudit.addContestCVRIds()` appends all rounds' draws to a single
accumulated field with no round tag. The SQL exports the full accumulated list
regardless of which round's file you requested. Per-round selection files are
therefore nearly or completely identical across rounds.

**Bug 2 — `contest_comparison.sql` attributes CVRs to every contest on a ballot.**
`cvr_contest_info` fans out to every contest printed on a ballot, and the join
to `comparison_audit` is a `LEFT JOIN` that never filters rows. Every CVR
audited for contest A appears in the comparison export for contests B, C, D...
(all contests on that ballot). On a typical Colorado general election ballot
with ~26 contests, each audited CVR produces ~26 comparison rows, of which
~25 are spurious.

**Both bugs are confirmed export-only.** They do not affect the risk-limit math,
sample counts, discrepancy tallies, or audit status — only the CSV/report layer.
See the [GitHub issue](https://github.com/loriinboulder/colorado-rla/issues)
for full technical detail, proposed SQL fixes, and live reproduction steps.

## Survey results

`check_corla_exports.py` was run against every round in this archive for which
both a selection and comparison file are available (23 rounds, 2019–2025).

**Every single round is affected by both bugs.**

| Metric | Total |
|--------|------:|
| Rounds with comparison file | 23 |
| Rounds with sel\_only > 0 (Bug 1 signal) | 23 / 23 |
| Rounds with cmp\_only > 0 (Bug 2 signal) | 23 / 23 |
| Total sel\_only (selected, no audited comparison) | 64,017 |
| Total cmp\_only (comparison attributed to wrong contest) | 1,743,228 |
| Affected contest-rounds | 10,216 |

`sel_only` counts CVR IDs in `contestSelection` for a contest that have no
corresponding audited comparison record. `cmp_only` counts CVR IDs in
`contestComparison` for a contest that are not in that contest's selection
list — these are spurious Bug 2 rows.

The Bug 1 cross-round identity check found that 99–100% of contests have
identical selection IDs between consecutive rounds for every multi-round audit,
confirming the accumulated-list export rather than a per-round slice.

Rounds without a comparison file in the archive (not analysed):
2022 general r1, 2023 coordinated r1/r2, 2024 primary r1.

## Fixability

**Bug 2 is fully correctable from the archived files.**
The correct filter is: keep only comparison rows where the `cvr_id` appears in
that contest's `contestSelection` entry for the same round. The selection file
is the authoritative draw list; the correction is lossless (every removed row
is a spurious attribution). See `correct_comparison.py`.

*WIP:* The corrector script is functional for individual round pairs but a
batch mode covering all 23 rounds, and a detailed accounting of what changed
in each corrected file, is still in progress. The corrected files have not yet
been committed to this repository.

**Bug 1 is not correctable from the archived files alone.**
The per-round selection files are nearly identical across rounds; there is no
way to reconstruct which CVR IDs were added in each round without the server's
internal `comparison_audit.contest_cvr_ids` data at each round boundary.
Single-round audits (the majority) are unaffected in practice.

## Planned extensions (WIP)

- **Level 2 statistics**: recompute discrepancy counts and Kaplan-Markov
  p-values per contest per round using the corrected comparison data. The
  colorado-rla formula is `Audit.pValueApproximation()` in `Audit.java`,
  implementing equation (10) of Stark's *Super-Simple Simultaneous
  Single-Ballot Risk-Limiting Audits* with γ = 1.03905.
- **Batch corrected exports**: run `correct_comparison.py` over all 23 rounds
  and commit corrected files alongside originals.
- **Cross-audit trend report**: visualise sel\_only and cmp\_only counts over
  time across elections.

## Files

| File | Description |
|------|-------------|
| `check_corla_exports.py` | Fetches selection and comparison files from this repo and reports sel\_only / cmp\_only counts per contest per round, plus Bug 1 cross-round identity check. Run with `--verbose` for per-contest breakdowns. |
| `correct_comparison.py` | Filters a `contestComparison.csv` to remove Bug 2 spurious rows, using the corresponding `contestSelection.csv` as the authoritative draw list. Accepts `--round 2024/general/round1` to fetch directly from this repo, or `--selection` / `--comparison` for local files. |

## Usage

```
# Survey all archive rounds (fetches from GitHub, takes ~5–8 min):
python3 check_corla_exports.py

# Verbose: per-contest breakdown for every affected contest:
python3 check_corla_exports.py --verbose

# Correct the Bug 2 comparison file for a specific round:
python3 correct_comparison.py --round 2024/general/round1 --output corrected.csv

# Or from local files:
python3 correct_comparison.py \
    --selection contestSelection.csv \
    --comparison contestComparison.csv \
    --output contestComparison_corrected.csv
```
