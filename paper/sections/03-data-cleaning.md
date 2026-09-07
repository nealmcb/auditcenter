<!--
Draft prose for §3 (Data cleaning & normalization). Written already
anonymized for double-blind review: no author names, no repo URLs, no
first-person "I/we built" framing tied to a specific person. Most of §3 is
original empirical work with nothing external to cite -- no \cite{} keys
were needed here (unlike §2 and §5). Reconfirm that's still true before
final submission, per the double-blind rule in ../README.md.

Rough length: ~1,750 words, targeting the outlined 3.5-page budget in
two-column 10pt format. Trim/expand once it's actually laid out.
-->

# 3. Data cleaning and normalization

Colorado has published machine-readable risk-limiting audit (RLA) data for
every statewide and coordinated election since 2017 — fourteen election
instances spanning ten years. No single, uniform dataset spans that
period, however: the state's audit software and its export conventions
changed repeatedly, sometimes within a single election cycle, and the raw
exports themselves carry data-quality issues of several distinct kinds.
This section describes those changes and issues
and how they have been normalized into a uniform schema with mappings
back to the original data.

Note also that San Juan County hand-counts its ballots, and does not produce
cast-vote records at all. It has not participated in the CVR-based comparison audit this paper's data
comes from. San Juan's ballots are excluded from every count in this paper for that reason.

## 3.1 Fourteen elections, three export eras
[TODO: note that the CORLA software exports files which are then
manually moved into the auditcenter web site. Automating this procedure
would help speed the process up and regularize the file naming.]

[TODO: round-by-round reporting is a bigger, separate topic than this
section currently lets on -- found real prior work, not yet reflected
here. Checked against the private analysis repo directly, not guessed:
this is NOT incomplete human export work, it's a confirmed CORLA software
behavior. `ComparisonAudit.addContestCVRIds()` always *appends*, so
`contest_cvr_ids` accumulates across rounds rather than resetting --
every round's export of that field reflects the FINAL accumulated state,
not that round's own selection. A second, compounding bug: the
comparison-file SQL joins on `audit_reason` rather than contest identity,
so any ballot drawn for any same-type targeted contest gets logged
against every contest on that ballot, not just the one it was drawn for.
Documented in `SELECTION_FLAWS.md` (a worked example: Pueblo County
Commissioner - District 2, 2024 general, all three rounds show byte-
identical files) and `SELECTION_FLAWS_SURVEY.md` (systematic sweep: 22 of
22 audited rounds, 2019-2025, show at least one of these two symptoms).
No draft SoS/CDOS feedback document was found under that description --
searched, doesn't appear to exist yet, or exists somewhere not checked.
Open decision, not resolved here: does this paper (a) ignore round-level
granularity entirely and describe only final-round/cumulative state
throughout (already the closest thing to current practice — see
`DATA_DICTIONARY.md`'s "always prefer the final/highest-round-number
version" note), (b) allude to it briefly as a known limitation without
detail, or (c) treat it as substantive enough for its own subsection --
each has different implications for §3's "three export eras" framing and
for §4-6's round-handling assumptions.]

The audit software's own export format falls into three structurally
distinct eras. The earliest, used for the 2017 coordinated election, the
2018 primary, and the first three rounds of the 2018 general election, is
a raw per-cast-vote-record "ballot list" — one row per examined ballot
(scanner, batch, and record identifiers, an imprinted ballot ID, and a
binary examined/not-examined flag, but no recorded contest choice), with
no contest-level parameter file and no standardized per-contest
comparison export at all. The 2018 general election's own final round is
a partial exception: it does carry a contest-level parameter file with aggregate
discrepancy-type counts, and a per-ballot file recording the audit board's
own read of each examined ballot — but that per-ballot file has no column
recording the voting system's own choice for the same ballot, so it
supports aggregate counts but not a genuine two-sided, ballot-by-ballot
comparison the way every later year's export does. The great majority of
the fourteen elections, from 2019 onward, use a "contest CSV" era: a
per-contest parameter file (`contest.csv` and its several later
renamings), a per-contest, per-jurisdiction mapping file, and a genuine
two-sided CVR-vs-audit-board comparison file. [TODO shouldn't we just ignore or avoid describing this even this much?] Starting with the 2025 CORLA
support for auditing Instant-Runoff Voting (IRV) via a different
statistical framework (RAIRE-style IRV assertions), rather than
Kaplan-Markov comparison auditing, another minor column-name/order change happened.

Even within the "contest CSV" era, filenames and directory conventions
vary far more than the underlying column structure does. The per-contest
parameter file alone appears under a variety of distinct filenames across
the surveyed elections (`contest.csv`, `ContestList.csv`,
`ContestsListRound1.csv`), and the comparison file under four
(`contestComparison.csv`, `contest_comparison.csv`, `contest_detail.csv`,
`CVRtoAuditBoardInterpretationComparison.csv`) — but most of that churn is
cosmetic: of the seven file types this schema relies on, five keep
exactly the same columns across every election that has them, despite
being renamed three to five times apiece. The comparison file itself only
changes shape twice in ten years, not once per rename: the 2018 general
election's version lacks a column for the voting system's own choice
entirely (the two-sided-comparison gap already noted above), and the 2022
primary is the first to add a trailing `audit_reason` column, which every
comparison file since has carried. Round-numbered directories are named
`round_1`/`round_2`/`round_3` in earlier years and `round1`/`round2`/`round3`
(no underscore) in later ones; two elections publish a single, unnumbered
`finalReports` directory instead.

To reconcile this we built an explicit, per-election layout
table — one small record per election instance naming which filename,
directory, and column conventions that instance actually uses.
This allows records in the final database rows to reference the exact data they are based on.

A separate limitation, orthogonal to format variation, is that this
reconstruction draws on an archive built by repeatedly downloading CORLA's
published exports over time, not a continuous capture of every version of
every file. Some files — ballot manifests in particular — can be revised
more than once during an active audit cycle as errors are found and
corrected, and a snapshot taken between revisions is not guaranteed to be
the first version, the last version, or the corrected one. §3.4 documents
a concrete case where exactly this pattern combined with a limitation in
our own download process to leave a manifest mislabeling uncorrected in
the archive well after it was fixed at the source.

## 3.2 Contest identity: fragmentation and name-variant resolution

A second source of complexity is contest identity itself.
The only current way to set the sample size in each county via CORLA
is to target a contest and use the global risk limit chosen for all contests
targed in the election. But there is often not a suitable county-level contest
available. So sometimes the department of state splits a statewide contest
into uses the vote counts
within an individual county for a statewide contest to calculate a margin
.

CORLA sometimes reports what is, substantively, one contest as several
separate rows in the per-contest parameter file: one "bare" row for the
contest as a whole, plus one or more county-suffixed rows when that
contest's ballot pool in some particular county was too small to support an
adequate sample there on its own, forcing a county-specific sub-sample.
This pattern — found in five of the eleven checkable election instances —
appears under a variety of naming conventions across those five
(`"<Contest> (<County>)"`, `"<Contest> - <County> County"`, and
`"<Contest> - <County>"`.

The distinction matters beyond bookkeeping. Each county-suffixed fragment
carries its own `audit_reason` and its own record of whether *that
fragment's* sub-sample reached its risk limit — and that per-fragment
status must never be read as if it were the true, whole contest's status.
An analysis that queries a fragment's own "risk limit achieved" field
without first resolving it back to its parent contest will systematically
over- or under-count how many real contests were adequately audited,
because a fragment succeeding or failing says nothing directly about the
other fragments of the same true contest. The normalized schema described
in §3.5 resolves this by construction: every raw parameter-file row is
retained (so no figure is ever un-traceable to its literal source row), but
a separate consolidation pass — run once, at import time, for every
election — groups fragments back to one true-contest record per real
contest, and every downstream table reports only on actual contests.

## 3.3 An unintentional, fully recoverable remapping of ballot identifiers

The most striking single data-cleaning problem solved in this
reconstruction was an unintentional remapping of ballot identifiers,
confined to specific export files, that turned out to be entirely
recoverable once its mechanism was understood. Colorado's ballot-
identifier convention is a hyphen-separated triple,
`{tabulator}-{batch}-{position}` (for example, `4-5-69`). In eight of the
fourteen election instances, a substantial minority of these identifiers
instead appear in the comparison export as `M/D/YYYY`-formatted dates —
for example, `4/5/1969` in place of `4-5-69`.

The mechanism is demonstrable, not merely plausible. Common spreadsheet
software's short-date autodetection reads a hyphenated three-number string
as a month-day-year date whenever the first number is a valid month (12 or
less) and the second a valid day (31 or less), converts it to an internal
date value, and re-emits it in slash-separated form on save, applying a
standard two-digit-year century window along the way — an ordinary,
well-known spreadsheet behavior, not anything particular to elections
data. One of the earliest-era files in the dataset happens to carry the
true tabulator, batch, and record numbers in separate columns *alongside*
the remapped identifier in the same row, which makes the mechanism
directly verifiable rather than inferred: reversing the transformation on
every affected row in that file reproduces the other three columns'
values exactly, with zero exceptions across dozens of rows. Because the
remapping only triggers when both the tabulator and batch numbers happen
to fall within valid date ranges, its incidence varies sharply by county —
from under 15% to over 75% of rows in different counties of the same
election — purely as a function of each county's own tabulator- and
batch-numbering scheme.

Across the full survey (roughly 1,300 candidate files scanned), the
remapping appears in exactly the elections using one of three older
comparison-file names, and is entirely absent, across several hundred
thousand examined ballots, starting with the election that first adopted
the current comparison-file name — consistent with an incidental change
somewhere in the export or publication pipeline at that point, though
nothing in the exported data itself can establish exactly what changed or
when. That is not a question this paper attempts to resolve; the more
useful fact for this paper's purposes is that the remapping is fully
reversible and, once corrected, recovers every one of these identifiers
exactly.

The practical value of finding this is straightforward: every remapped
identifier would otherwise fail exact-string comparison against
correctly-formatted values elsewhere in the same dataset (the ballot
manifest, the state's own record of which identifiers were selected for
audit), which is what first drew attention to it during selection-
reproduction checks. The fix is narrow and reversible — detect the
date-shaped pattern within the known remapping window and invert it,
leaving every already-correctly-formatted identifier (the overwhelming
majority) untouched — and was verified against the one file where ground
truth is independently recoverable before being applied across the full
dataset. With it applied, every one of these ballot identifiers is
recovered exactly, adding a meaningful share of previously-unmatchable
records back into the usable evidence base described in §5.

## 3.4 Manifest export: mislabeling, gaps, and recovery

Ballot manifests are deliberately independent of the voting system by
rule, not merely by incidental county practice: "the county must maintain
an accurate ballot manifest in a form approved by the Secretary of State
and independent of the voting system" \cite{corules2026}. That
independence is what makes the manifest a genuine, separate check on the
tabulator's own count rather than an echo of it — but it also means each
county's own manifest-producing process, not a single state-mandated
format, determines the file this paper's reconstruction has to parse.

Each county's manifest totals reach this reconstruction through two
channels: a standalone per-county manifest export, and a per-batch
manifest-vs-CVR comparison file every county also files, which happens to
carry the same underlying manifest totals alongside a parallel,
CVR-derived count for the same batches. Both describe the same
county-reported data; the second is simply a convenient secondary route
to the same manifest totals when the standalone export is unavailable.

A separate category of gap affects the ballot manifests themselves.
Comparing manifest files byte-for-byte
across counties surfaced an instance in 2025 when we pulled the auditcenter
at a point in time when the exported Montrose manifest was actually a
copy of the Montezuma manifest. The actual sampling data reveals that
the audit was working from distinct manifests, since Montrose's sampled
ballots are from tabulator 103, which does not show up in Montezuma's manifest.
So this was clearly
an issue with the manual construction of the auditcenter itself,
and our scraping software at the time skipped files that
had already been downloaded, and wouldn't catch manual fixes to
the export files in auditcenter that came later.

One full election instance was found to have no per-county manifest files
published at all; a second was missing manifests for six of sixty-three
counties. In both cases, the per-batch manifest-vs-CVR file described
above allowed those gaps to be closed with totals that match the state's
own published aggregate figures exactly, applied county by county rather
than as an all-or-nothing fallback, after an earlier all-or-nothing
version of the recovery was itself found to be incomplete against
affected files that had already been recovered from independent web
archive captures.

## 3.5 Normalized schema for TODO [TODO insert name of resulting database]

The result of resolving §§3.1–3.4 is a TODO [TODO insert name of resulting database], with a single relational schema spanning
all fourteen election instances, built around one election dimension that
every other table references, an explicit true-contest/raw-fragment split
that enforces the distinction in §3.2 structurally, and per-row provenance
(the literal source filename, and for several tables the full original raw
row) retained alongside every derived field, so that any figure quoted from
the normalized data remains traceable back to its literal origin. Three
election instances prior to 2019 that use the earliest "ballot list" export format
populate only the manifest-level tables, rather than forcing a
fit into a contest-level schema those exports were never structured to
support; one further instance's IRV audit is scoped out of
the risk-bearing tables for the same reason. Nothing in the schema silently
drops a known gap — every exclusion in this section is recorded explicitly,
as a property of a specific election instance, rather than left for a
downstream query to rediscover by absence.
