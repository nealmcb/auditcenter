# Best practices for round-by-round audit observability

## Why this matters

Colorado's RLA exports are the primary public record of how each audit
proceeded. The selection and comparison files are intended to let anyone
independently verify that the correct ballots were drawn and correctly
compared. This verification only works if the exports faithfully represent
what happened in each round, and if anyone can determine what was new in each
round versus what carried over.

The system supports this — but only if exports are taken at the right moment.

## How the export works

The download-audit-report endpoint runs live SQL queries against the current
database state and streams the result into a zip file. It has no concept of
"round" — there is no parameter to request a specific round's data, and no
snapshot logic. Every call returns the current accumulated state.

The per-round directory structure in the Audit Center archive (`round_1/`,
`round_2/`, etc.) is created by SOS staff manually downloading the report
package at points during the audit and filing the files into the appropriate
directory. The software does not do this automatically.

## The critical timing rule

**The round-N export must be downloaded after all round-N ballots have been
submitted and before round N+1 is launched.**

`contest_cvr_ids` (the accumulated selection list) is extended at the
**start** of each round, before any auditing begins. If the export is
downloaded after round N+1 has launched — even seconds after — the
"round N" selection file already contains round N+1's draws. Because the
SQL dumps the full accumulated list with no round filter, those draws are
indistinguishable from round N's.

Evidence in the archive: in nearly every multi-round audit, round N and
round N+1 selection files are 99–100% identical. This indicates the exports
were taken after the next round had already launched, or that
no new draws were needed (risk limit already achieved for all contests).

## Round-by-round diffing

Given correctly-timed exports, the round-by-round evolution of the audit is
fully visible by diffing consecutive selection files:

- **Round N selection minus round N−1 selection** = the new draws for round N
  (the incremental sample required because the risk limit had not yet been met)
- **Round N comparison minus round N−1 comparison** = the audit board
  interpretations submitted during round N

Both diffs should be non-empty (there would be no reason to start round N
without new draws or new auditing). If they are empty or nearly empty, it
indicates either that the export timing was wrong, or that all contests had
already achieved their risk limit and round N involved only completing
ballots already in progress.

## What is currently missing from the exports

**Multiplicity is not exported.** Colorado RLA samples with replacement: the
same ballot can be drawn more than once, and each draw counts independently
in the Kaplan-Markov risk product. The Java model tracks this in
`CVRAuditInfo.multiplicity_by_contest` and `count_by_contest`. However, the
comparison SQL uses `SELECT DISTINCT`, collapsing multiple draws of the same
CVR into a single row. An external verifier cannot reproduce the exact KM
calculation from the comparison file alone when any CVR has multiplicity > 1.

**Round provenance is not in the selection file.** The selection file is a
single JSON array of CVR IDs with no indication of which round each ID was
added. Correctly-timed snapshots can substitute for this (diffing consecutive
round files gives the per-round incremental draws), but this requires
disciplined export timing as described above.

## Recommended operational procedure

1. Complete all ballot submissions for round N (all audit boards finish and
   sign off their ballots for the round).
2. Download the full report package **before** launching round N+1.
3. Archive the downloaded files in a round-specific directory (e.g.
   `round_N/`).
4. Only then launch round N+1.

This procedure requires no software changes. It produces a self-consistent
record at each round boundary:
- The selection file at round N reflects exactly the draws for rounds 1
  through N.
- The comparison file at round N reflects exactly the audited interpretations
  for rounds 1 through N.
- Consecutive selection files correctly diff to show round N's incremental
  draws.

## Note on phantom ballots

A ballot marked `PHANTOM_BALLOT` (physical ballot not found) breaks the
system's internal "audited prefix" count, which determines the starting
position for the next round's draws. CVRs listed after the first phantom in
the sequence are re-added to the next round's draw even if they have already
been audited. This can cause the selection file to accumulate CVR IDs that
appear unaudited (`sel_only > 0`) in ways that persist across rounds and
survive into the final export. This is a known open issue in the comparison
SQL (noted as a TODO in the source) and is independent of export timing.
