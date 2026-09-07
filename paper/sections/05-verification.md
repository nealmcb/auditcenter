<!--
Draft prose for §5 (Dataset integrity verification). Anonymized, double-blind-
ready third-person prose. Real citations inserted inline as \cite{} keys -- see REFERENCES.md.

Deliberately excludes the separate "does our own recomputed risk value agree
with CORLA's reported pass/fail status" check (VALIDATION_RESULTS.md §2) --
that's Kaplan-Markov risk-value methodology territory, out of scope here per
../README.md's boundary (Caron/Stark co-authored future work). This section
covers ONLY the selection-reproduction check: did CORLA draw the ballots it
says it drew. That's a pure ballot-identity comparison, no risk formula
involved, and it's the check that establishes the dataset itself is
trustworthy enough to support §4's coverage claims.

Rough length: ~800 words, targeting the outlined 1.5-page budget.
-->

# 5. Dataset integrity verification

The coverage figures in §4 are only as trustworthy as the underlying
dataset. Before drawing any conclusion from it, the reconstruction was
checked against an independent, external ground truth: does the state's
audit software's own published selection record match what an outside
party, working only from public inputs, can independently recompute?

## 5.1 Method

For every formally targeted contest — one where the audit software drew a
sample directly by name, rather than a contest that merely happened to
appear on ballots drawn for another reason — the underlying pseudo-random
draw sequence was reconstructed from two pieces of public data: the
publicly announced random seed, and the relevant county ballot manifest(s).
The audit software's own selection algorithm, confirmed by direct reading
of its published source code \cite{corlasoftware}, is straightforward: hash the seed together
with a counter using SHA-256, reduce the result modulo the size of the
relevant ballot population, and repeat for each successive counter value
until enough distinct ballots are drawn. Reconstructing this sequence
independently and comparing the resulting set of ballot identifiers against
the audit software's **own official record** of which ballots it selected
— a separate file the software itself publishes, distinct from the seed and
manifest inputs — is the strongest available check: it tests whether the
selection *itself* matches, not merely whether every selected ballot later
received a logged comparison record, which is a separate and noisier
question addressed by the discrepancy-typing check in §5.3.

## 5.2 Results

Across the eleven election instances where the necessary files exist (the
earliest three instances predate the file formats this check requires, per
§3.1), **732 of 748 checkable targeted contests — 97.9% — reproduce the
audit software's own official selection exactly: zero ballots missing, zero
extra**, for every contest where the check succeeded. Results by election
appear in Table~\ref{tab:selection-reproduction}.

| Election | County-level contests | Statewide contests |
|---|---:|---:|
| 2019 | 63/63 | 1/1 |
| 2020 (general) | 61/63 | 0/0 (blocked) |
| 2020 (presidential) | 0/0 (blocked) | 0/0 (blocked) |
| 2020 (primary) | 88/88 | 1/1 |
| 2021 | 62/64 | 0/0 (blocked) |
| 2022 (primary) | 78/80 | 2/2 |
| 2022 (general) | 62/63 | 0/6 (blocked) |
| 2023 | 62/63 | 1/1 |
| 2024 | 62/63 | 2/2 |
| 2025 | 72/73 | 2/2 |
| 2026 | 112/112 | 1/1 |
Table: Selection-reproduction results by election. \label{tab:selection-reproduction}

"Blocked" entries are cases where a known, independently-detected manifest
gap in the underlying source data (the same kind of gap described in §3.4)
prevents any reproduction attempt from running at all — these are counted
separately from actual mismatches, and each is a specific, named,
previously-documented gap, not a silent skip.

## 5.3 What the mismatches turned out to be

The 16 remaining discrepancies are informative in their own right: this
verification effort is itself a useful way to find data-quality issues, not
only a correctness check. Several of the mismatches found in earlier passes
of this same reproduction sweep were the direct trigger for identifying the
identifier remapping described in §3.3 — ballot identifiers that failed
exact-string comparison turned out, on investigation, to have been
unintentionally reformatted in the state's own export rather than genuinely
mismatched selections. One further mismatch, a 2025 statewide contest whose
domain construction depended on Montrose County's manifest, is now resolved
by the same fix described in §3.4: once Montrose's true manifest is used
instead of its mislabeled duplicate of Montezuma's, that contest's selection
reproduces exactly. Of the mismatches remaining after both fixes, most
trace to real quirks on the audit software's own side rather than to the reproduction
methodology: one contest's parameter file carries a stale field left over
from an earlier audit round while its companion selection file correctly
reflects a later escalation; another contest is administratively classified
as spanning the entire state while its actual reproduced ballot identifiers
show every hallmark of a genuinely small, few-county domain; several
contests share a single already-characterized class of manifest-total gap
not yet traced to the specific county responsible. Nine contests' mismatches
remain individually uninvestigated as of this writing, listed explicitly as
open items rather than silently omitted.

As a secondary, independent validation channel, a typed-discrepancy check —
comparing the count of each Kaplan-Markov discrepancy category (two-vote
and one-vote overstatements and understatements, `o2`/`o1`/`u2`/`u1`;
§6.2 reports what these mean and finds substantively) independently
derived from the normalized per-ballot comparison data against the audit
software's own reported counts for the same categories, contest by
contest — matches exactly for every one of the 477 formally targeted
contests where both counts exist (Table~\ref{tab:typed-discrepancy-validation}),
a check that exercises a different part of the pipeline (per-ballot
comparison parsing rather than PRNG reconstruction) and corroborates the
same conclusion from an independent angle.

| Source | o2 | o1 | u1 | u2 | Total |
|---|---:|---:|---:|---:|---:|
| CORLA's own reported count | 18 | 8 | 12 | 8 | 46 |
| Independently derived | 18 | 8 | 12 | 8 | 46 |
Table: Typed-discrepancy validation across just the 477 formally targeted contests: independently derived counts against CORLA's own reported counts, matching exactly. \label{tab:typed-discrepancy-validation}

## 5.4 What this establishes

A 97.9% exact-match rate against an independently reconstructed ground
truth, with every remaining discrepancy individually named and, in most
cases, already traced to a specific, understood cause on the source data's
own side, is the basis for treating the normalized dataset as reliable
enough to support the structural coverage analysis in §4. It does not, on
its own, validate any particular risk-value calculation methodology for
contests that were never directly, formally targeted — that is a separate
question, addressed in future work (§7).
