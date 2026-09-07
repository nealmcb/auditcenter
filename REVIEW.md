# Academic review: EVT/WOTE 2026 Colorado audit case study

## Recommendation

**Major revision required before submission.**

This is a promising and unusually useful data-reconstruction paper, but the
checked-in artifact is still a working draft rather than a submission-ready
paper. Its strongest contribution is the normalized, cross-election account of
what CORLA's public exports contain. The paper should keep that structural
scope and avoid implying that opportunistically covered contests have received
the same statistical guarantee as targeted contests.

## What is strong

- The paper states a focused research question and distinguishes targeted,
  opportunistically named, and no-comparison-record contests
  (`paper/sections/04-coverage.md:25-42`).
- The coverage table is explicit: 6,522 contests are classified, with 477
  directly targeted and 5,645 opportunistically named
  (`paper/sections/04-coverage.md:58-82`).
- The selection check is substantially better than an unsupported claim:
  it describes the public inputs, the independent reconstruction, blocked
  cases, and the 16 remaining mismatches
  (`paper/sections/05-verification.md:25-98`).
- The discrepancy section correctly distinguishes comparison rows from
  physical ballots and warns that a single wrong-ballot incident can create
  many discrepant rows (`paper/sections/06-discrepancies.md:38-68`,
  `:125-135`).
- The manuscript is candid about the unresolved 20-row discrepancy-report
  reconciliation (`paper/sections/06-discrepancies.md:177-229`). That
  uncertainty should remain prominent rather than being hidden in a footnote.

## Blocking revisions

1. **The submitted artifact is not yet a clean paper.** The source contains
   TODO notes, planning comments, and editorial instructions in the sections
   themselves, including unresolved text in the conclusion
   (`paper/sections/07-conclusions.md:20-35`) and questions about what to
   include in the data-cleaning section
   (`paper/sections/03-data-cleaning.md:1-48`). Remove all working notes from
   the submitted source and regenerate the PDF from that cleaned source.

2. **The page-limit claim is unverified and currently over budget.**
   `paper/OUTLINE.md:18-21` estimates 13.5--14 pages against a 12-page
   maximum and explicitly says that a real layout pass is still pending.
   Build the actual PDF, record the body and bibliography page counts, and
   cut or move material before submission.

3. **The paper's data and analysis are not self-contained.** The build
   documentation says the headline tables read an 800+ MB database from the
   sibling private repository (`paper/README.md:61-66`), while the referenced
   `paper/scripts/` directory is absent on this branch. A reviewer cannot
   reproduce the reported 6,522-contest, 97.9%-selection, or 965,254-row
   figures from this checkout. Publish a suitably sized, versioned analysis
   input or archive, the exact scripts, schema, and generated-table commands;
   otherwise label the paper as an analysis of an unavailable companion
   dataset and state precisely what can be independently checked here.

4. **The verification denominator needs a complete audit trail.** The paper
   reports 732/748 exact matches, but the table includes blocked cells and the
   prose says nine mismatches remain uninvestigated
   (`paper/sections/05-verification.md:47-73`, `:84-98`). Add a machine-readable
   contest-level ledger identifying every success, blocked case, mismatch,
   source-file version, and reason. Explain why 748 is the correct denominator
   and reconcile the stale 97.7% figure still present in
   `paper/OUTLINE.md:14`.

5. **The discrepancy results mix incompatible coverage scopes.** The 644
   comparison discrepancies cover ten election instances, while the 811
   reason-attributed rows cover eight and the independent reconciliation
   yields 814 rather than 834 (`paper/sections/06-discrepancies.md:70-92`,
   `:107-123`, `:188-204`). Add a single scope table showing which elections,
   source reports, row types, and exclusions feed each headline number.
   Reconcile the 644/811/814 figures and explain whether “rate” means rows,
   physical ballots, or incidents in every table and abstract statement.

6. **The conclusion currently makes claims the paper says are out of scope.**
   It presents opportunistic risk-level calculation and shared-seed
   dependence as substantive conclusions (`paper/sections/07-conclusions.md:22-44`),
   even though `paper/README.md:44-59` explicitly holds that methodology out.
   Either supply and review the required statistical derivation or reduce this
   to a clearly bounded future-work paragraph. Do not suggest that the
   structural coverage counts establish risk limits for opportunistic
   contests.

7. **Double-blind compliance is incomplete.** The README requires neutralizing
   author names, identifying acknowledgements, and self-citations
   (`paper/README.md:31-42`), but the repository includes correspondence,
   provenance notes, named contributor references, and author-identifying
   material outside the generated body. Inspect the PDF metadata and every
   packaged file, remove identifying material from the submission archive,
   neutralize self-citations, and make a separate non-blinded artifact for
   archival use.

## Required final checks

- Regenerate `paper/latex/corla_10.pdf` from a clean checkout and inspect the
  output for unresolved TODOs, broken references, overfull layout, and page
  count.
- Run the analysis from a documented, immutable input snapshot and preserve
  the exact generated tables used in the PDF.
- Add references for every external method, statute, software implementation,
  and source archive; verify that each citation supports the sentence where it
  appears.
- Provide contest- and election-level appendices or downloadable tables for
  the coverage, selection-verification, and discrepancy claims.
- State limitations prominently: missing early comparison formats, blocked
  manifest cases, unresolved mismatch causes, unavailable private inputs, and
  the 20-row discrepancy-report gap.
- Perform a final secret scan and PDF metadata scan on the complete submission
  bundle, not just on the LaTeX body.

