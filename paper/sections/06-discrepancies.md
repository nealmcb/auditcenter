<!--
Draft prose for §6 (Discrepancies) -- NEW section, added 2026-09-04 per
Neal ("add a section on discrepancies. That's probably most useful data
here. unfortunately with some gaps so far"). Inserted between Verification
(§5) and Conclusions (renumbered §6 -> §7). Anonymized, double-blind-ready
third-person prose.

Sourced entirely from auditcenter_analyze-private's
DISCREPANCY_TYPE_REASON_REPORT.md, which already does real, honest,
cross-validated work here -- this section largely condenses it. All
numbers double-checked against that doc's own tables, using its own
stated preference for its corrected/reconciled figures (811/814) over the
older previously-published ones (834) where the two differ, per that
doc's own "Reconciliation findings" section.

Stays structural/descriptive throughout: what discrepancies were found, at
what rate, attributed to what cause, by two independent classification
systems -- never a risk-value or risk-limit-achieved claim. This is
importantly DIFFERENT from the held-out opportunistic risk-calculation
methodology (Caron/Stark territory) -- discrepancy counts are direct
audit-board findings, not a computed risk metric, so this section doesn't
need to touch that boundary at all. Double-checked this distinction
explicitly before writing.

Rough length: ~1,450 words, ~2.5-3 pages.
-->

# 6. Discrepancies

A key question for both the public and those designing auditing methods
is: *how often do discrepancies of various types occur, and why*?
Colorado's data provides new insights for this question, based on
how often the audit board's physical read of a ballot disagreed with the voting system's own
interpretation, what kind of disagreement it was, and why they might have occurred.

## 6.1 Method

CORLA's comparison export records, for every examined ballot-contest pair,
both the voting system's own recorded choice and the audit board's own
hand interpretation; a genuine discrepancy exists exactly when the two
disagree in a way that isn't itself an artifact of the export or a
software display quirk (a small number of purely cosmetic candidate-name-formatting
mismatches found in one election's export were confirmed as such and
excluded, both here and from CORLA's own reported counts for that
election).
After each election, the Department of State also publishes a post-audit discrepancy report,
after asking the counties to provide ballot images for each ballot that had a reported
discrepancy.
That report assigns a *reason category* based on their estimation
of the most likely explanation for each discrepancy, for
example, "Wrong Ballot," "Audit Board Error," or "Ambiguous Voter Intent".

Every genuine discrepancy was classified two ways. First, by
the Department of State categorization (when we had a copy of it),
and second, by its Kaplan-Markov *type* — a two-vote or one-vote overstatement or
understatement (conventionally `o2`/`o1`/`u2`/`u1`) relative to the
specific winner/loser pair the audit's risk calculation tracks for that
contest, or no type at all when the mismatch doesn't touch that tracked
pair (most commonly because the contest is uncontested, so no loser exists
to assert against).

These two classifications answer different questions — one is
a process explanation, the other feeds into the risk limit calculations.
§6.3 shows how they relate. Throughout, "examined" denotes a
contest-ballot comparison row, not a distinct physical ballot; a single
ballot contributes one row per contest it carries (§2), so the
denominator below is substantially larger than the number of physical
ballots actually pulled.

## 6.2 Overall rate

Across every election with ballot-level comparison data (2018 general
plus every "contest CSV"-era election, ten instances in all — §3.1),
**644 genuine discrepancies were found across 965,254 examined
contest-ballot comparisons, an overall rate of 0.067%** — broken down by
Kaplan-Markov type and by election in Table~\ref{tab:discrepancy-typing-by-election}.

| Election | o2 | o1 | u1 | u2 | Total | Examined | Rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 general | 6 | 3 | 0 | 3 | 12 | 164,796 | 0.0073% |
| 2020 (primary) | 16 | 4 | 4 | 16 | 40 | 61,546 | 0.0650% |
| 2020 (general) | 59 | 68 | 71 | 62 | 260 | 234,333 | 0.1110% |
| 2020 (presidential) | 0 | 0 | 0 | 0 | 0 | 155 | 0.0000% |
| 2021 | 5 | 11 | 12 | 5 | 33 | 60,597 | 0.0545% |
| 2022 (primary) | 6 | 8 | 8 | 8 | 30 | 118,827 | 0.0252% |
| 2023 | 5 | 3 | 9 | 2 | 19 | 35,486 | 0.0535% |
| 2024 | 47 | 52 | 65 | 61 | 225 | 149,272 | 0.1507% |
| 2025 | 4 | 6 | 4 | 4 | 18 | 47,706 | 0.0377% |
| 2026 (primary) | 5 | 0 | 0 | 2 | 7 | 92,536 | 0.0076% |
| **Overall** | **153** | **155** | **173** | **163** | **644** | **965,254** | **0.0667%** |
| Overall rate | 0.0159% | 0.0161% | 0.0179% | 0.0169% | — | — | 0.0667% |
Table: Two- and one-vote overstatement (o2/o1) and one- and two-vote understatement (u1/u2) discrepancy counts and rates by election. 2019 coordinated and 2022 general are excluded here (source data not further categorized -- §6.4); 2017 pilot, 2018 primary, and 2020 presidential's own predecessor formats have no comparison data at all (§3.1). \label{tab:discrepancy-typing-by-election}

The rate varies
by roughly a factor of twenty across elections, from a low of 0.0073%
(2018 general) and 0.0076% (2026 primary) to a high of 0.151% (2024
general) and 0.111% (2020 general) — the two largest general elections in
the survey, where both the absolute count and the denominator are largest.
One instance (2020 presidential, a small two-contest election) shows zero
discrepancies of any kind out of 155 examined rows. No secular trend
across the ten-year window is apparent; the two general elections have
consistently higher rates than the primaries and coordinated elections
surrounding them, more consistent with general elections' higher overall
ballot volume and complexity than with any change in audit-process
quality over time.

## 6.3 What causes discrepancies

For the eight elections where the we captured the Department of State's
discrepancy report (2020 primary through 2026 primary),
811 discrepancies were attributed to a specific
process cause. **A single cause dominates: "Wrong Ballot" — the audit
board physically retrieved a different ballot than the one the system
selected — accounts for 532 of 811 (65.6%)**, more than three times the
next-largest category, "Audit Board Error" (171, 21.1%, a case where the
correct ballot was retrieved but its interpretation was mis-recorded).
Every other category is comparatively rare: "Voting System Limitation" (an
uncorrected undervote the system cannot resolve, 41, 5.1%), "Adjudication
Error" (a tabulation-judge misjudgment during canvass, 38, 4.7%),
"Ambiguous Voter Intent" (12, and a further 4 recorded under a near-
identical, differently-worded category, together 2.0%), and five further
categories each appearing in only one or two elections, together under 1%
of the total.

Part of Wrong Ballot's dominance by row count, rather than by underlying
incident, is a structural artifact of what "examined" means here (§6.1):
a single misretrieved ballot produces one discrepant comparison row for
*every* contest that ballot carries, so one wrong-ballot mistake on a
long ballot can register as a dozen or more discrepant rows, while a
single Audit Board Error or Adjudication Error typically misjudges just
the one contest under review. The reason-category counts above are
therefore counts of discrepant rows attributable to each cause, not
counts of independent human or process mistakes — Wrong Ballot's true
share of underlying incidents, as opposed to rows, is not established
here.

The two classification systems interact informatively. Of 307 two-vote
discrepancies (the more severe category, a complete swap between a
winner and loser), Wrong Ballot accounts for 222 (72.3%) and
Audit Board Error for 83 (27.0%) — together over 99%, essentially the only
two causes capable of producing a full name-for-name swap, since both
mechanisms substitute one specific candidate's choices for another's
wholesale. One-vote discrepancies (324 total, a lesser swing toward or
away from "neither") are less lopsided: Wrong Ballot still leads (196,
60.5%), but Adjudication Error's share jumps to 10.5% (34) from its
essentially negligible 0.3% share of two-vote cases — consistent with a
tabulation judge's misjudgment on a hard-to-read mark typically nudging a
reading toward or away from no-selection, rather than flipping it to the
opposing candidate outright. "Voting System Limitation" never produces a
two-vote discrepancy at all (0 of 41), and over half of its rows (24 of
41) register no Kaplan-Markov type whatsoever; tracing those 24 directly
shows 21 are contests with only one candidate ever recorded anywhere in
the vote totals — mechanically uncontested, so no winner/loser pair can
exist for the classifier to assign a type against, regardless of what the
ballot itself shows.

The comparison-audit literature sets a rough expectation for how one-vote
and two-vote counts should relate, specifically for overstatements: a
one-vote overstatement is an ordinary byproduct of how voters mark paper
ballots — "occasional one-vote misstatements are expected, owing to the
vagaries of how voters mark their ballots: from time to time the system
will interpret a light mark as an undervote or a hesitation mark as an
overvote" — while a two-vote overstatement, a full swap from one
candidate to another, "should be quite rare," and "generally... indicates
a programming error..., fraud, or other serious problem"
\cite{lindeman2012gentle, stark2010supersimple}. This dataset's own o1
and o2 counts are close in magnitude rather than o2 being negligible by
comparison (155 and 153 overall, Table~\ref{tab:discrepancy-typing-by-election}) — consistent with
our finding that most genuine two-vote discrepancies trace to "Wrong Ballot"
or "Audit Board Error". These are process failures the cited literature's
"programming error, fraud, or other serious problem" framing did not
anticipate as the typical cause. Finding the right ballot, especially
when the unique "imprinted id" is not physically imprinted on the ballot,
requires counting thru the batches of ballots by hand, and an error
compounds, as noted above.

## 6.4 Data-quality gaps in the discrepancy record itself

Consistent with our approach elsewhere (§3, §5), we checked the
discrepancy record itself against an independent source rather than
taking it at face value, precisely because §6.3's reason-category
findings depend on it: if the underlying row counts were wrong, so would
be everything built on top of them. The check did not pass cleanly. We
care about this specifically because the affected elections are the same
ones cited by name in §6.3, so a reader relying on those numbers deserves
to know exactly how far they can be trusted, not a vague disclaimer.

A from-scratch re-derivation of the same underlying Secretary of State
reports, performed independently of an earlier published tally of the
same eight elections, reproduces four of the eight exactly but comes up
20 rows short across the other four (814 versus 834 total, a 2.4% gap):

| Election | Independently re-derived | Previously published | Gap |
|---|---:|---:|---:|
| 2020 (primary) | 119 | 122 | −3 |
| 2020 (general) | 276 | 280 | −4 |
| 2021 | 38 | 44 | −6 |
| 2022 (primary) | 86 | 93 | −7 |
| 2023 | 22 | 22 | exact |
| 2024 | 235 | 235 | exact |
| 2025 | 22 | 22 | exact |
| 2026 (primary) | 16 | 16 | exact |
| **Total** | **814** | **834** | **−20** |
Table: Reconciliation of the independently re-derived discrepancy-report row counts against an earlier published tally of the same eight elections. \label{tab:reconciliation-gap}

One genuine parsing bug was found and fixed in the course of this check —
a case-sensitivity error that had silently dropped 16 rows from the 2020
primary's report, since that one election's document happens to render
"Audit board error" in lowercase where every other year capitalizes
it — and is already reflected in the 814 figure above.

Beyond that fix, the remaining 20-row gap across four elections
(Table~\ref{tab:reconciliation-gap}) was pursued hard and not resolved.
Two independent checks, each using a method structurally unrelated to
the original parsing, corroborate the lower, re-derived figures rather
than the higher, previously-published ones. First, 2022 primary's entire
source report — both of its rendered pages — was independently
re-transcribed row by row, by a second pass with no access to the
parsing code, tallying each category by hand from the rendered text
rather than trusting the parser's own extraction; that from-scratch count
also came to 86, matching the parser exactly, category by category, not
merely in total. Second, 2021's count was checked against a completely
different data source: a separate method that derives genuine
discrepancies directly from raw ballot-level comparison data (CVR versus
audit-board interpretation), built independently of this report and
without reference to the Secretary of State's own published document at
all, also finds exactly 38 genuine discrepancies for that election — the
same lower figure, reached by a method with no shared code or logic with
the PDF parser to have propagated a shared bug.

Most strikingly, in three of the four mismatching elections (2020
primary, 2021, 2022 primary), *every single reason category* is short by
exactly one row relative to the originally published total — not
concentrated in any particular category, which would be the more typical
signature of a single missed or double-counted row. 2020 general breaks
this pattern only slightly: four of its five categories are short by
exactly one row, while its "Adjudication Error" category matches the
published total exactly. This "off by exactly one, spread evenly across
categories" signature was actively hunted for a mechanical cause —
whether a table row could have split silently across a page boundary,
whether two physical rows could have been merged into one extracted
text line, whether an alternate spelling of a category name could have
been miscounted, whether a column mixup (confusing a "Target Contest"
flag with an actual "Discrepancy" flag) could explain it — and none of
these explains the pattern. The independent row-by-row re-transcription
of 2022 primary's own source pages, described above, found no missing
rows there either: the source document itself, read directly, supports
86, not 93.

One concrete, untested hypothesis remains open: 2022 primary's own
report text refers to "the report labeled CVR to audit board
interpretation comparison (Round 2)" as "the original version of the
report used" — language suggesting the earlier published tally may have
been built from a different or earlier version of that same source
document, one not retained in this reconstruction's own archive, rather
than from the version available to us. A related possibility is that the
earlier tally counted a subtly different thing — for instance, every row
flagged as a "Target Contest" rather than only rows specifically flagged
as a "Discrepancy." Neither possibility is confirmed; both remain open
questions a direct request to the state for its own original working
file could likely resolve.

Given the multiple, methodologically independent corroborations of the
lower figures and the inability to locate a further parsing bug despite
real effort, we report the independently re-derived counts throughout
§6.3 rather than the original published ones. The unresolved 20-row gap
is reported here explicitly, not silently absorbed into either number —
a specific, well-defined discrepancy, not a vague caveat, and one a
direct follow-up with the state could likely resolve.

Coverage of the discrepancy record is also structurally incomplete in
ways independent of that reconciliation gap. The three earliest-era
election instances (§3.1) carry no ballot-level comparison data of any
kind and are entirely absent from every count above. Two further election
instances have real, importable comparison data but are deliberately
excluded from the polished figures in §6.2–§6.3 because their underlying
source files are documented elsewhere as raw exports never further
categorized by the state, with one specifically flagged for a known
candidate-ordering software artifact that needs that same qualification
attached every time its numbers appear. One further election's data structurally excludes one county's
ballots entirely, pending resolution of an open question about that
county's relationship to the rest of the dataset. And one instance (2018
general) has only an aggregate, contest-level discrepancy-type count
available, with no per-ballot reason-category data of any kind — real
numbers, but a coarser measurement than every other election in this
section.
