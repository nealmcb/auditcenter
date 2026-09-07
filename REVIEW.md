# Academic review: *Colorado Risk-Limiting Audits: Three Years In*

## Recommendation

**Reject in the present form; invite resubmission after major revision.**

This submission is a 22-page slide deck rather than a research paper. It
contains useful descriptive material about Colorado's early risk-limiting
audits (RLAs), but it does not provide the scholarly apparatus, methods, or
reproducibility materials needed to support its claims.

## Summary and contribution

The deck describes ballot-polling and ballot-level comparison RLAs, then
plots counts of CVRs, audited ballot cards, discrepancies, and audit rounds
for five elections from 2017 through the 2020 presidential primary. It also
classifies discrepancies and argues that county performance improved over
time. A public archive of the underlying Colorado Audit Center material is
valuable, and the deck could become a useful case study or data note.

## Major concerns

1. **The central quantitative results are not reproducible from the
   submission.** The figures contain plotted values but no tables, data
   extracts, code, formulas, contest-level inclusion criteria, or mapping
   from source files to the plotted aggregates. The repository contains
   spreadsheets, PDFs, HTML snapshots, and two data-recovery scripts, but no
   analysis program for the deck. Running the scripts does not reproduce the
   figures: they are recovery/download utilities and one requires network
   access. The paper should provide a versioned machine-readable dataset and
   a deterministic analysis script or notebook.

2. **The unit of analysis and denominators are ambiguous.** “Number of CVRs,”
   “ballot cards audited,” “discrepancies,” and “number of rounds” are
   presented as election totals, but the deck does not say whether these are
   sums across counties, target contests, or audit rounds; how duplicate
   cards/contests are handled; or how counties unable to participate are
   treated. The 2020 presidential-primary archive explicitly records Adams
   County as completing a separate audit, so the treatment of that county
   must be stated. “Discrepancies per card” also needs an exact definition
   and denominator.

3. **The longitudinal inference is confounded and unsupported.** The claim
   that counties became more accurate or efficient is not identified by the
   descriptive plots. Election type, number of counties, contest margins,
   voting systems, audit software versions, ballot volume, training, and
   the composition of sampled contests all change over time. A lower
   discrepancy rate could reflect easier contests or different sampling,
   not learning. Report uncertainty and stratified results, and separate
   operational learning from election-level composition effects.

4. **The discrepancy taxonomy is not operationalized.** Categories such as
   “audit board error,” “wrong ballot,” and “voting system limitation” need
   coding rules, adjudication procedures, mutually exclusive/exhaustive
   status, and a record-level provenance trail. The statement that no
   voting-system tabulation error occurred is important, but the deck does
   not provide the records or investigation protocol needed to evaluate it.

5. **The statistical audit context is incomplete.** The deck explains the
   mechanics at a high level but does not report risk limits, stopping rules,
   contest margins, sample-size calculations, or the RLA statistical methods
   used. Consequently, readers cannot assess whether the reported audit
   outcomes support the stated confidence claims.

6. **There are no scholarly references.** Neither the PDF nor the repository
   provides a bibliography, DOI/citation list, or references to the relevant
   RLA literature, statistical tests, election rules, or Colorado software
   specifications. The repository README links to project and software
   documentation, including the ColoradoRLA export manual and related
   repositories, but those links are not a substitute for citations in the
   submission. The cited CORLA link should also be checked and replaced with
   a stable URL if necessary.

7. **Presentation and terminology need editorial revision.** The document
   has slide-deck fragments (“Links from a previous slides”), inconsistent
   grammar, and technical wording that can mislead readers (“the system does
   not tabulate correctly, but it is still working as intended”; “out stack”).
   Define CVR, ballot card, manifest, discrepancy, and contest universe once,
   and provide accessible tables alongside the charts.

## Reproduction attempt

I inspected `OverviewThreeYearsIn.pdf`, the README, the archived audit
artifacts, and both Python utilities. The PDF text confirms the five
elections, the four principal metrics, the discrepancy categories, and the
zero-discrepancy statement for the 2020 presidential primary, but its charts
do not expose the underlying numeric series. The repository has no script
that computes those series. Therefore I could not independently regenerate
the plotted values or verify the claimed trend from the supplied materials.

Some qualitative claims are consistent with the archive: the 2020
presidential-primary page notes that Adams County completed a separate audit
with no discrepancies, and the repository contains official audit reports
and discrepancy reports. That is not sufficient to validate the aggregate
figures or the causal conclusion.

## Double-blind review and author-identifying evidence

The artifact is **not suitable for double-blind review as submitted**:

- The PDF metadata contains `/Author(Edward Morgan)`.
- `observerfiles/evidence-timestamping.md:19-26` names Neal McBurnett, gives
  an email address, and links to the repository owner's GitHub account.
- The same document links the work to a personal CORLA website and personal
  social-media/timestamp records.
- `2026/primary/observerfiles/2026-primary-details.md:68-78` attributes
  collection and receipt-time attestation to named individuals.
- `recover_wayback_only_2022_2024.py:154` contains an explicit
  `Co-Authored-By` attribution.
- Git history also exposes a named commit author for the manuscript.

These disclosures should be removed from a blinded artifact, or the venue
should treat this as an openly identified data/software review rather than a
double-blind submission. The metadata author name should also be reconciled
with the manuscript's stated authorship.

## Required revisions

1. Recast the work as a paper, data note, or software/data report and state
   the research question and contribution precisely.
2. Add a references section covering RLA theory, Colorado rules, software,
   and every external data source.
3. Publish the exact input tables, schema, checksums/version identifiers,
   inclusion/exclusion rules, and a reproducible analysis script/notebook.
4. Give contest- and county-level tables with risk limits, margins, sample
   sizes, rounds, discrepancies, and discrepancy classifications.
5. Replace the causal “improved” conclusion with an appropriately qualified
   descriptive analysis, or supply a design that supports the stronger claim.
6. Document the discrepancy review protocol and preserve links from every
   categorized record to its source report.
7. Correct terminology, grammar, chart labels, and accessibility issues.
8. Produce a clean anonymized artifact without PDF metadata, personal links,
   named provenance, author-attributed commits, or other identity leaks.

