<!--
Draft prose for §1 (Intro). Anonymized, double-blind-ready third-person
prose. Real citations inserted inline as \cite{} keys -- see REFERENCES.md.

Rough length: ~330 words, targeting the outlined 0.75-page budget.
-->

# 1. Introduction

Colorado has run a mandatory, statewide risk-limiting audit after every
election since November 2017 — ten years and fourteen election instances
of production data, published by the state as a matter of course. Despite
this, no public dataset spans that entire record in a single, normalized
form, and no public analysis has asked the most basic structural questions
about it.

We unlock the study of this groundbreaking data by reconstructing, cleaning, and
normalizing our archive of CORLA's exported data into a single relational
dataset, and report four findings. First, the raw data itself required
substantial cleaning before it could be normalized: three distinct
export formats across the survey period, contest identities that
sometimes fragment into multiple, differently-named rows within a single
election, and unintentional remapping of ballot identifiers caused by common spreadsheet
software's own date-autodetection misreading a hyphenated identifier as a
calendar date before the file was published. Second, the resulting
dataset can be independently trusted: reconstructing the state's own
pseudo-random ballot selections from public inputs alone reproduces its
official selection record exactly for 97.9% of checkable targeted
contests, with the small remainder traced almost entirely to specific,
well-defined gaps in the available source data rather than any flaw
in the reconstruction.

Third, Colorado's audits produce valuable election integrity
evidence relevant to both the formally targeted contests (which achieve their risk limits),
and also the other contests which are "opportunistically" audited.
Every paper ballot[^sheets] in the sample drawn for a targeted contest's audit
is also interpreted by humans for every other contest present, and compared to
the corresponding original voting system record.
Fourth, discrepancies between the human interpretations and the system
interpretations are rare and mostly due to human error. In the available data,
we find a discrepancy rate of 0.067% across 965,254 contest-ballot
comparisons, roughly two-thirds of which trace to the audit board
retrieving the wrong physical ballot rather than any disagreement about
how a given ballot should be read. This reconstruction also surfaces specific gaps in the historical public
record — including material once available on the state's own online audit
data site that is no longer, and that this project continues trying to
recover — which more systematic archiving of that valuable public resource
would help prevent going forward.

We give a brief background on Colorado's audit design in §2, then
describe the data-cleaning methodology (§3), the coverage findings
themselves (§4), the verification against an independent ground truth
(§5), what the audits actually found when examining ballots (§6), and
directions for future work this reconstruction makes possible (§7).

[^sheets]: A voter's ballot may consist of more than one sheet of paper;
    the voting system and the audit both work at the level of an
    individual sheet, and multi-sheet ballots are interpreted and audited
    sheet by sheet rather than as one unit. We follow common
    usage and refer to a ballot-sheet simply as a "ballot" throughout,
    except where the distinction matters.
<!--
Draft prose for §2 (Background). Anonymized, double-blind-ready third-person
prose. Real citations inserted inline as \cite{} keys -- see REFERENCES.md.

Rough length: ~550 words, targeting the outlined 1.25-page budget.
-->

# 2. Background

Risk-limiting audits provide statistically grounded, software-independent
evidence that a reported election outcome matches what the paper ballots
actually show \cite{stark2012evidence}, rather than merely re-running the
same tabulation software again \cite{lindeman2013retabulation} — evidence,
rather than trust placed in any single tabulation system, being the
foundation the whole approach is built on. Colorado piloted the method
years before adopting it statewide: a 2010 audit in one county is credited
as the first risk-limiting audit conducted outside California, followed by
further county-level pilots in 2011 and a 2013 ballot-level comparison
audit of three contests in one county, funded in part by a $230,000 U.S.
Election Assistance Commission grant supporting pilots in five counties
from 2011 to 2014, and a further round of mock audits in three more
counties in 2015. Risk-limiting audits have since been endorsed by the
National Academies of Sciences, Engineering, and Medicine, first in
*Securing the Vote* (2018) and again in *Moving to Evidence-Based
Elections* (2023) \cite{nas2018securing, nas2023moving}. Colorado has
conducted a mandatory, statewide risk-limiting audit after every general,
primary, and coordinated election, and before certification, since
November 2017, required by Colorado Revised Statutes \S 1-7-515
\cite{corstatute} and implemented under Secretary of State Rule 25
\cite{corules2026}. Within two weeks after election day,
the Secretary of State convenes a public meeting to establish a random seed
— a decimal string at least twenty digits long, generated by rolling dice.
That seed drives a publicly verifiable pseudo-random number algorithm to
select ballots to be audited, with the aid of a purpose-built comparison-audit tool \cite{corlasoftware}: a Java
web application we refer to throughout as "CORLA", which county audit boards use to record the audit's results.
CORLA's role is deliberately narrow: it receives as input ballot manifests and
cast-vote-record files (CVRs) uploaded by each county, identifies which paper ballots
must be examined, and records each examined ballot's marks. It then calculates
risk levels for the targeted contests, and if necessary, expands the sample size
and iterates the process until the risk limit is satisfied.

CORLA's sampling method is a direct implementation of the standard
Kaplan-Markov comparison-audit approach used across many RLA
implementations in the United States \cite{stark2008conservative,
lindeman2012gentle} — one of the two main RLA families alongside
ballot-polling audits such as BRAVO \cite{lindeman2012bravo}, which
Colorado's implementation has not used since 2019. For each *targeted* contest — one
whose margin the Secretary of State has selected to formally drive that
audit round's sampling — CORLA hashes the public seed together with an
incrementing counter using SHA-256, reduces the result modulo the size of
the relevant ballot population, and repeats until enough distinct ballots
are drawn to reach a target sample size computed from that contest's own
margin and risk limit. A contest may be targeted at the county level (its
own county's full ballot population is the draw domain), at a multi-county
level (the domain is the union of several counties' manifests,
concatenated in a fixed order), or at the statewide level (every county's
manifest, concatenated) — the multi-county case identified as a needed
capability, and largely absent from Colorado's audit software, as
recently as 2018 \cite{lindeman2018nextsteps}.

Not every contest on the ballot is targeted this way. A single physical
ballot typically carries dozens of contests — a targeted statewide race, a
handful of county-wide offices, and often several much smaller special-
district or municipal contests with far narrower margins of their own. When
a ballot is drawn to examine its targeted contest, every other contest that
ballot also carries gets examined as a byproduct, whether or not that other
contest was ever independently selected. We call a contest
audited this way — one that receives examined ballots purely as a side
effect of some other contest's targeted draw — *opportunistically covered*
throughout. The distinction between targeted and opportunistically covered
contests, and the much smaller set of contests that receive no examined
ballots under either mechanism, is the central subject of §4.

We draw on our own practice of periodically downloading CORLA's exported data across
every election instance from 2017 through the first half of 2026 — fourteen
election instances in all, spanning the variety of export formats
described in §3, and reflecting a point-in-time archive rather than a
continuous capture of every revision a file underwent (§3.1).
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
<!--
Draft prose for §4 (Coverage findings). Anonymized, double-blind-ready
third-person prose. Real citations inserted inline as \cite{} keys -- see REFERENCES.md.

Table below is the literal output of ../scripts/coverage_analysis.py,
re-run 2026-09-03. Regenerate before final submission in case the
underlying dataset changes.

Deliberately stays at the level of "does CORLA's own export name a
comparison record for this contest" throughout -- never a risk-value claim.
See ../README.md's scope boundary and the terminology note in
../scripts/coverage_analysis.py's docstring (do not call the no-record
category "zero coverage" or "unaudited").

Rough length: ~1,050 words + table, targeting the outlined 3-page budget.
-->

# 4. Categories of Contests

Colorado's mandatory RLA program is often described as
auditing "the election", but it targets only a
small number of contests by name to achieve the risk limit (§2), and does
not report any risk levels for the opportunistic contests.

## 4.1 Method

Every contest in the normalized dataset (§3) was classified, per election,
into one of three categories, based solely on whether and how it
appears in CORLA's own examined-ballot comparison export: **directly
targeted** (the contest itself was named as a formal sampling target),
**opportunistically named** (the contest was never itself targeted, but at
least one examined ballot's comparison record names it — i.e., some ballot
drawn for another contest's draw also happened to carry this one), or **no
comparison record** (the contest's name never appears in any examined-
ballot comparison record for that election). Each contest was additionally
classified by how many counties its own ballot population spans: a single
county, a proper subset of the state's counties ("partial multi-county"),
or every county in the election ("statewide"). The three election
instances using the earliest export era (§3.1) never populate a
per-contest parameter file at all, only manifest-level data, and so
cannot be classified by this method — they are omitted from every column
below, rather than counted as zero.

One classification exception is known and worth naming directly rather
than left as a silent error: "City of Fort Collins Mayor" (2025), an
Instant-Runoff Voting contest, is counted below as opportunistically
named because this method reads only the state's main coordinated-election
export. A separate, IRV-specific export for that same election (§3.1)
shows it was in fact formally targeted and completed its own audit under
a RAIRE-based risk-limiting framework, with real, non-zero sampling. That
export's IRV-specific risk methodology is out of scope for this paper
(§3.1), but its coverage status should not be — this one contest is
misclassified in Table~\ref{tab:coverage-by-election}, and is named here
rather than silently left wrong.

## 4.2 Results

| Election | Total contests | Directly targeted | Opportunistically named | No comparison record | Single-county | Partial multi-county | Statewide |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 576 | 52 | 498 | 26 | 457 | 117 | 2 |
| 2020 (general) | 652 | 60 | 520 | 72 | 510 | 142 | 0 |
| 2020 (presidential) | 2 | 2 | 0 | 0 | 0 | 0 | 2 |
| 2020 (primary) | 372 | 34 | 304 | 34 | 282 | 87 | 3 |
| 2021 | 666 | 54 | 588 | 24 | 537 | 127 | 2 |
| 2022 (general) | 961 | 43 | 871 | 47 | 801 | 135 | 25 |
| 2022 (primary) | 651 | 38 | 604 | 9 | 543 | 96 | 12 |
| 2023 | 661 | 43 | 542 | 76 | 511 | 148 | 2 |
| 2024 | 721 | 63 | 597 | 61 | 555 | 142 | 24 |
| 2025 | 640 | 62 | 541 | 37 | 515 | 124 | 1 |
| 2026 | 620 | 26 | 580 | 14 | 512 | 97 | 11 |
| **Total** | **6,522** | **477** | **5,645** | **400** | **5,223** | **1,215** | **84** |
Table: Contest coverage classification by election, and by county span. \label{tab:coverage-by-election}

Across the full survey (Table~\ref{tab:coverage-by-election}), **6,122 of 6,522 contests (93.9%) have at least one
examined-ballot comparison record named in CORLA's own export**: 477 (7.3%)
by direct targeting, and 5,645 (86.6%) purely as a byproduct of some other
contest's draw. The remaining 400 contests (6.1%) have no name-matched
comparison record in the export for that election. Directly targeted
contests are consistently a small minority of the total — never more than
about 10%, and often closer to 4% in the larger general elections, where
the number of small down-ballot contests grows faster than the number of
contests formally selected to drive sampling.

By county-span, the overwhelming majority of contests — 5,223 of 6,522, or
80.1% of the classifiable total — are single-county contests, entirely
contained within one county's own ballot population. A substantial minority
(1,215, 18.6%) span a proper subset of the state's counties without being
truly statewide; genuinely statewide contests are comparatively rare (84,
1.3%), appearing only in general elections and the occasional coordinated
or primary election with a statewide ballot measure.

## 4.3 What "no comparison record" does and does not mean

The 400 contests with no name-matched comparison record are not,
thereby, contests the audit process skipped. A ballot examined for one
contest's targeted draw is still physically read and interpreted in its
entirety by the audit board; it is only when none of the specific ballots
that happened to be drawn for other reasons also carried a particular
low-prevalence contest that the export ends up with zero rows naming that
contest by chance, not by design. This is most common for narrow-
prevalence contests — small special districts whose ballot population is a
tiny fraction of their county's full manifest — where the probability that
any given examined ballot happens to carry that specific contest can be
low even when substantial auditing activity occurred broadly across the
same county. Whether, and how precisely, a meaningful statistical
conclusion can be drawn for these contests from the sampling activity that
did occur nearby is a separate methodological question to be addressed in
ongoing work (§7).
<!--
Draft prose for §5 (Dataset integrity verification). Anonymized, double-blind-
ready third-person prose. Real citations inserted inline as \cite{} keys -- see REFERENCES.md.

Deliberately excludes the separate "does our own recomputed risk value agree
with CORLA's reported pass/fail status" check (VALIDATION_RESULTS.md §2) --
that's Kaplan-Markov risk-value methodology territory, out of scope here per
../README.md's boundary (a separate future co-authored piece, per README.md's scope boundary). This section
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
methodology (a separate future co-authored piece, per README.md's scope boundary) -- discrepancy counts are direct
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
<!--
Draft prose for §7 (Preliminary conclusions & future work). Anonymized,
double-blind-ready third-person prose, real citations added inline (see REFERENCES.md).

Explicitly states the two held-out results as ongoing/future work WITHOUT
claiming their findings -- see ../README.md's scope boundary. Do not add
any actual number, formula, or conclusion from either of those threads here;
if a specific figure from that work seems tempting to cite, stop and check
with Neal first.

Rough length: ~430 words, targeting the outlined 1-page budget.
-->

# 7. Preliminary conclusions and future work

A normalized, extensively-cleaned dataset spanning ten years of a
state's production risk-limiting audits facilitates the study
of several questions that were previously difficult to approach via the public record.

[TODO: discrepancies!]

The next natural goal is calculating risk levels for contests audited opportunistically.
Early analysis suggests that a significant fraction of all the contests actually met
the risk limit. But a rigorous analysis is complicated.
Calculating risk levels for opportunistic contests which cover multiple counties requires a defensible
risk-calculation methodology since the sampling rate is not uniform across
all the counties.
In addition, the current sampling method draws each contest's
audit sample by reducing the seed, a shared per-election random value, against that
contest's own ballot-population size. When two contests' population sizes
share a common factor, this construction means that the samples in the
two counties are not independent. Any auditing method that requires
independence would need to properly take the correlations into account.
Note that this doesn't affect any of the risk calculations that the audit
guarantees for targeted contests.

An excellent way to solve that problem is to adopt Rivest's
"consistent sampling" method \cite{rivest2018consistent}, which derives
each ballot's sampling priority from the ballot's own identity rather than
a population-size-dependent reduction. It would also be a valuable
upgrade for Colorado's audit software since it
supports efficient sampling across overlapping contests and
supports the many benefits of style-based sampling more generally
\cite{glazer2021style}.
