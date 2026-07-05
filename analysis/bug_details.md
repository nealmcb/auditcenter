# `contestSelection.csv` / `contestComparison.csv` don't reconcile — two SQL export bugs, confirmed live and in production data (2019–2025)

## Summary

Colorado's Audit Center exports two CSV files per audit round for each contest:
`contestSelection.csv` (the CVR IDs drawn by the SHA-256 PRNG for that contest)
and `contestComparison.csv` (the CVR-level comparisons the audit board actually
submitted). They should reconcile: every selected CVR ID should eventually get
a comparison record, and every comparison record should trace back to a
selection.

They don't. Two independent SQL bugs in
`server/eclipse-project/src/main/resources/sql/` cause this, and both are
reproducible on demand, not one-off data glitches. A statistical survey across
22 real audit rounds (2019–2025) found **22/22 rounds affected**, with 869
contest-rounds showing `sel_only > 0` (ballots drawn but never audited per the
export) and 9,148 contest-rounds showing `cmp_only > 0` (comparison records
that don't trace to a selection).

**Good news: both bugs are confirmed export-only.** They do not corrupt the
actual risk-limiting audit math — verified directly against the live
`comparison_audit` / discrepancy tables, not just inferred from code reading.
The audit engine's own internal accounting (sample counts, discrepancy
tallies, risk status) is correct in every case checked; only the CSV/report
layer misrepresents it.

---

## Real-world example: Pueblo County Commissioner - District 2 (2024 General)

All three round exports for this contest are identical:

| File | CVR IDs |
|------|---------|
| `contestSelection.csv` | 378 |
| `contestComparison.csv` | 193 |
| In both | 189 |
| Only in `contestSelection` (selected, no comparison) | 189 |
| Only in `contestComparison` (comparison, not selected) | 4 |

Archived production data: https://github.com/nealmcb/auditcenter

---

## Bug 1 — `contest_selection.sql` has no round filter; exports the cumulative all-rounds list

`server/eclipse-project/src/main/resources/sql/contest_selection.sql`:

```sql
SELECT
   cr.min_margin,
   cr.contest_name,
   ca.contest_cvr_ids
FROM
   comparison_audit AS ca
LEFT JOIN
   contest_result AS cr
   ON ca.contest_result_id = cr.id
;
```

`ComparisonAudit.addContestCVRIds()` always **appends** to `contest_cvr_ids`,
once per round start (`StartAuditRound.makeSelections()`), and never resets or
tags entries with a round number:

```java
// ComparisonAudit.java
public void addContestCVRIds(final List<Long> contestCVRIds) {
    this.contestCVRIds.addAll(contestCVRIds);  // always appends, never replaces
}
```

Since `contest_selection.sql` has no round column or filter, it always dumps
the full accumulated field, regardless of which round's export you asked for
— which is why archived per-round files come out identical.

**Mechanism, reproduced live:** if a round-1 discrepancy grows the required
sample size (`optimisticSamplesToAudit()`), round 2 is started, new CVR IDs
are appended immediately — before the audit board has touched any of them —
and if the audit is interrupted before those round-2 ballots are submitted,
the export already shows them as "selected."

### Live reproduction

Using a synthetic single-contest county audit (`GrowRound`, diluted margin
0.05, 200 ballots):

1. Round 1 drew 75 ballots. Audited all 75, with **one deliberate 2-vote
   overstatement** injected on the lowest-margin assertion.
2. Sign-off recalculated the requirement: `optimistic_ballots_to_audit: 96 →
   233`.
3. Round 2 started — `comparison_audit.contest_cvr_ids` grew from 97 to 234
   raw entries (138 distinct CVR IDs) **immediately on round start**, before
   any round-2 ballot was audited.
4. Stopped there — no round-2 ACVRs submitted (simulating an interrupted
   audit).

Running the live, unmodified `contest_selection.sql` and `contest_comparison.sql`
at that checkpoint and diffing by CVR ID:

| | count |
|---|---|
| Distinct CVR IDs in `contest_selection.sql` output | **138** |
| Distinct CVR IDs with a genuine (audited) comparison record | **75** |
| `sel_only` (selected/exported, never audited) | **63** |

All 63 are verifiably round-2's newly-drawn, not-yet-audited ballots — not
"ballot doesn't contain this contest" (ruled out by construction: every
ballot in this county carries the contest).

**Caveat for anyone re-running this diff methodology:** `contest_comparison.sql`
emits a row for a CVR as soon as it's selected into a round's sequence
(`cvr_audit_info` row created at round-start), *before* the audit board
submits anything — such rows have `NULL` `audit_board_selection` / `consensus`
/ `timestamp`. A naive "does this CVR ID appear anywhere in the comparison
export" check undercounts `sel_only`; filter on a non-null result column
(e.g. `timestamp IS NOT NULL`) to count only genuine comparisons.

### Proposed fix

A SQL-only fix can suppress the specific reconciliation-diff symptom (slicing
`contest_cvr_ids` to its first `audited_sample_count` entries), but **this is
not a complete fix**. The file's own header states its purpose is
"verification of the random selection procedure" — i.e. an outside party
should be able to recompute the full PRNG draw and confirm the entire
announced sample, independent of whether the audit board has worked through
it yet. Slicing to `audited_sample_count` makes the export always lag reality
instead of distinguishing "drawn, pending" from "drawn, audited" — and it
still can't reconstruct true historical per-round selection lists after the
fact, since `audited_sample_count` is a single current-state counter, not an
append-only per-round history.

**A fully correct fix requires persisting a round number alongside each entry
in `contest_cvr_ids`** (or an equivalent per-round table) — i.e. a change to
`ComparisonAudit.addContestCVRIds()` / the persisted representation, not just
the SQL. Flagging that explicitly rather than shipping a SQL patch that only
half-solves it.

---

## Bug 2 — `contest_comparison.sql` attributes ballots to the wrong contest

`server/eclipse-project/src/main/resources/sql/contest_comparison.sql`
(relevant fragment):

```sql
LEFT JOIN
   contest_to_audit AS cta
   ON (cci.contest_id = cta.contest_id or cn.name = (select cn1.name from contest cn1 where cn1.id=cta.contest_id))
LEFT JOIN
   comparison_audit AS cpa
   ON cpa.audit_reason = cta.reason and cast (cci.cvr_id as TEXT) = ANY (
       string_to_array(substring(cpa.contest_cvr_ids from 2 for (char_length(cpa.contest_cvr_ids)-2)), ','))
```

### Live reproduction, and a correction to the join-key diagnosis

Two same-county `COUNTY_WIDE_CONTEST` contests draw from an **identical PRNG
domain** — the domain is the whole county's ballot count regardless of which
specific contest, and `SHA-256(seed + "," + count)` depends only on seed and
position, not contest identity. So a landslide contest needing few samples
and a tight-margin contest needing many samples in the same county pull from
the same underlying random stream, and the smaller contest's draw is a subset
of the larger one's.

Built exactly that: `TightRace` (diluted margin 0.067, 67 distinct CVRs drawn)
and `Landslide` (diluted margin 0.933, 7 distinct CVRs drawn, all ⊆
TightRace's 67) in the same county, both present on every ballot.

Running the live, unmodified `contest_comparison.sql` filtered to
`contest_name='Landslide'`:

| | count |
|---|---|
| Landslide's own `contest_cvr_ids` (ground truth) | **7** |
| Distinct CVR IDs `contest_comparison.sql` reports for Landslide | **67** |
| `cmp_only` (reported under Landslide, never drawn for Landslide) | **60** |

All 60 are exactly the CVRs drawn only for TightRace. Example row from the
live export:

```
Adams,Landslide,1-1-2,Ballot 1 - Type 1,Land1,Land1,YES,uploaded,,2026-07-03 21:46:47.6...,1616,COUNTY_WIDE_CONTEST
```

CVR 1616 was drawn and audited for TightRace only, but is attributed to
Landslide, with `audit_reason=COUNTY_WIDE_CONTEST` inherited from
*TightRace's* `comparison_audit` row.

**Important correction to the root-cause diagnosis:** the `audit_reason`
match is real and does corrupt the exported `audit_reason` column, but **it
is not what causes the extra rows to appear at all**. The join to
`comparison_audit` (`cpa`) is a `LEFT JOIN`. Tracing the query's `FROM`
chain: `cvr_audit_info` (one row per *audited CVR*) joins to
`cvr_contest_info` with no contest filter, so it returns one row **per
contest actually printed on the ballot** — regardless of which contest the
CVR was drawn for. Since every ballot here carries both contests, *any*
audited CVR — whether drawn for TightRace or Landslide — already produces
both a TightRace row and a Landslide row **before the `cpa` join is even
evaluated**. The `cpa` join only ever populates the (cosmetic) `audit_reason`
column; being a `LEFT JOIN`, it never gates which rows appear.

Verified directly: patching *only* the join key (from `audit_reason` to
contest identity, keeping it a `LEFT JOIN`) left row counts **completely
unchanged** (Landslide still showed 67 rows) — it only changed the
`audit_reason` value on the spurious rows to `NULL`. A working fix needs
**both** the corrected join key **and** a join type that actually filters.

### Proposed fix

```diff
  LEFT JOIN
-   contest_to_audit AS cta
-   ON (cci.contest_id = cta.contest_id or  cn.name = (select cn1.name from contest cn1 where cn1.id=cta.contest_id))
- LEFT JOIN
-   comparison_audit AS cpa
-   ON cpa.audit_reason = cta.reason and cast (cci.cvr_id as TEXT) = ANY (string_to_array(substring(cpa.contest_cvr_ids from 2 for (char_length(cpa.contest_cvr_ids)-2)), ','))
+   contests_to_contest_results AS ctcr
+   ON ctcr.contest_id = cci.contest_id
+ INNER JOIN
+   comparison_audit AS cpa
+   ON cpa.contest_result_id = ctcr.contest_result_id and cast (cci.cvr_id as TEXT) = ANY (string_to_array(substring(cpa.contest_cvr_ids from 2 for (char_length(cpa.contest_cvr_ids)-2)), ','))
```

`contests_to_contest_results` (`contest_id → contest_result_id`, `contest_id`
unique) already exists in the schema and is exactly the contest-identity
mapping needed; `contest_to_audit`/`cta` and the `audit_reason` match are
dropped entirely. The `LEFT JOIN → INNER JOIN` change is what actually
excludes ballot/contest pairs that were never drawn for that specific
contest.

**Verified live:** after this patch, `contest_comparison.sql` gives Landslide
exactly 7 rows (`cmp_only=0`), TightRace exactly 67 (`cmp_only=0`), and
`GrowRound` (Bug 1's contest, unaffected/orthogonal) unchanged at 138. As a
side effect, this also fixes the separately-documented symptom of untargeted
contests getting spurious comparison rows — with no `comparison_audit` row to
`INNER JOIN` against, they correctly produce zero rows.

---

## Does either bug affect the actual audit, or is it export-only?

Checked directly against the live `comparison_audit` and
`contest_comparison_audit_discrepancy` tables — the tables that actually
drive `ComparisonAudit`'s in-memory risk-limit computation:

```
 contest_name |  id  | audited_sample_count | optimistic_samples_to_audit | audit_status         | two_vote_over_count | disagreement_count
 GrowRound    | 2260 |                    97 |                          233 | IN_PROGRESS          |                    1 |                   0
 TightRace    | 2232 |                    73 |                           72 | RISK_LIMIT_ACHIEVED  |                    0 |                   0
 Landslide    | 2249 |                     7 |                            6 | RISK_LIMIT_ACHIEVED  |                    0 |                   0

 contest_comparison_audit_discrepancy:
 contest_comparison_audit_id | discrepancy | cvr_audit_info_id
 2260                        | 2           | 1929
```

- **Bug 2 — export-only, confirmed.** Landslide's own `audited_sample_count`
  is 7 (not 67), and its discrepancy counters are all zero. The
  `contest_comparison_audit_discrepancy` ledger — the table actually
  consulted for risk computation — has exactly one row, belonging to
  GrowRound only. None of the 60 spuriously-exported ballots ever touched
  Landslide's or TightRace's real accounting. `isCovering()` /
  `signalSampleAudited()` correctly gate the math.
- **Bug 1 — export-only, confirmed.** GrowRound's own `comparison_audit` row
  honestly reports `audit_status=IN_PROGRESS`, `audited_sample_count=97` (not
  138 — it does not count the unaudited round-2 draws as done), and
  `optimistic_samples_to_audit=233`. The state-admin dashboard reflects this
  correctly and never claims the audit is complete or the risk limit met.

**Conclusion: both bugs are confirmed pure export/reporting defects. Neither
corrupts the risk-limiting audit's statistical guarantees or its live
accounting of what has/hasn't been audited** — but they do actively mislead
anyone using `contestSelection.csv` / `contestComparison.csv` for external
verification or transparency purposes, which is the entire point of
publishing them.

---

## Reproducing this

1. Upload CVR + manifest data for one county with two (or more) plurality
   contests present on every ballot — one tight-margin, one landslide-margin
   — to get a deterministic subset relationship between their PRNG draws for
   Bug 2. Use a separate county/contest with a single contest for Bug 1.
2. Define the audit, select all contests as `COUNTY_WIDE_CONTEST`, enter a
   seed, start round 1.
3. For Bug 1: audit round 1 completely but inject one deliberate discrepancy
   on the lowest-margin assertion to grow the required sample size, sign off
   the round, start round 2, then stop before submitting any round-2 results.
4. For Bug 2: audit both contests' full round-1 draws normally (no
   discrepancy needed).
5. Run `psql -f contest_selection.sql` and `-f contest_comparison.sql`
   against the live DB and compare against `comparison_audit.contest_cvr_ids`
   (ground truth) — filtering the comparison export to rows with a non-null
   `timestamp` to exclude selected-but-not-yet-audited placeholder rows.

---

## Scope note

Both proposed fixes above are scoped to
`server/eclipse-project/src/main/resources/sql/contest_selection.sql` and
`contest_comparison.sql` only. No Java/model code was changed. As noted
above, the Bug 1 SQL fix is a partial mitigation, not a complete fix — a full
fix needs per-round tracking added to `ComparisonAudit`/`contest_cvr_ids`,
which is out of scope for a SQL-only patch and is called out here rather than
silently underdelivered.

A related, lower-priority, structurally distinct issue was also identified
but not the focus of this report: `ContestCounter.countAllContests()` groups
contests by `contest().name()` alone with no county scope, so two counties
using an identical un-prefixed contest name string would be silently merged
into one cross-county draw (confirmed present in code; a concrete near-miss
was found in 2024 production data where Garfield County omitted its county
prefix, though no actual name collision occurred that year). Filing
separately if wanted — flagging here for completeness since it was found in
the same investigation.
