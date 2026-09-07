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
