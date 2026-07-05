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

They don't, due to two independent bugs in the server SQL. Full technical
detail, live reproduction steps, and proposed SQL fixes are in
[`bug_details.md`](bug_details.md).

Note: file names, directory layouts, and CSV header names have varied across
audit years (e.g. `contestSelection.csv` vs `contest_selection.csv`,
`round_1` vs `round1`). This complicates full automated reproduction and
correction across the archive; `check_corla_exports.py` handles the known
variants, but the accounting may be incomplete for years not yet tested.

**Bug 1 — `contest_selection.sql` has no round filter.**
`ComparisonAudit.addContestCVRIds()` appends all rounds' draws to a single
accumulated field with no round tag. The SQL exports the full accumulated list
regardless of which round's file you requested. Per-round selection files are
therefore nearly or completely identical across rounds.

**Bug 2 — `contest_comparison.sql` attributes CVRs to every contest on a ballot.**
`cvr_contest_info` has one row per (CVR, contest) for every contest printed on
a ballot. The join to `comparison_audit` uses a `LEFT JOIN` that never filters
rows. As a result, any CVR audited for contest A appears in the comparison
export for every other contest on that ballot — whether or not it was drawn for
those contests.

An important nuance: contests that share the same PRNG domain (e.g., two
county-wide contests in the same county, or two statewide contests) draw from
the same underlying random sequence, so the smaller contest's sample is a
subset of the larger contest's sample. CVRs drawn for the larger contest but
not the smaller will be spurious in the smaller contest's comparison export.
Contests with *different* PRNG domains do not share this systematic subset
relationship, though they can still produce spurious rows via the
`cvr_contest_info` fan-out for any ballot type on which both contests appear.

**Both bugs are confirmed export-only.** They do not affect the risk-limit
math, sample counts, discrepancy tallies, or audit status — only the CSV/report
layer.

## Definitions

- **sel\_only**: CVR IDs that appear in `contestSelection.csv` for a contest
  but have no corresponding audited comparison record in `contestComparison.csv`
  (identified by a non-null `timestamp` in the comparison file). These are
  drawn ballots with no submitted audit board interpretation — expected at
  round end for unfinished audits, but also inflated by Bug 1 when next-round
  draws have already been appended before auditing begins.

- **cmp\_only**: CVR IDs that appear in `contestComparison.csv` for a contest
  but are not in that contest's `contestSelection.csv` entry. These are the
  primary Bug 2 signal: comparison records attributed to a contest the CVR was
  never drawn for.

- **aff\_c** (affected contests): contests in a round where either sel\_only
  or cmp\_only is nonzero.

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
| Affected contest-rounds (aff\_c summed) | 10,216 |

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

*WIP:* The corrector script is functional for individual round pairs. A batch
mode covering all 23 rounds, including handling of filename and header
variations across years, is still in progress. Corrected files have not yet
been committed to this repository.

**Bug 1 correction is also being explored (WIP).** The Colorado RLA PRNG is
deterministic given the public seed and ballot manifest, both of which are
archived here. Recalculating the per-round draws from the PRNG — rather than
relying on the accumulated `contestSelection` files — may allow reconstruction
of true per-round selection lists. This is tractable for single-round audits
and for identifying which contests gained new draws between rounds; the work
of determining exact round boundaries for multi-round escalations is ongoing.
See also the [rlauxe](https://github.com/JohnLCaron/rlauxe) repository for
related prior work.

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
| `bug_details.md` | Full technical write-up: root-cause analysis, live reproduction steps, proposed SQL fixes with diffs, and confirmation that both bugs are export-only. |

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
