# Paper outline

**Working title:** "Ten years of Colorado audits thru 2026"

Solo-authorable scope only -- see README.md's "Scope boundary" before adding
anything about risk-value calculation methodology or CVR-provenance tooling.

| § | Content | Source material | Pages | Status |
|---|---|---|---|---|
| 1. Intro | Motivation: no public systematic accounting of CO RLA data across 13+ elections; four headline findings previewed | New writing | 0.75 | Drafted |
| 2. Background | CO RLA design basics -- targeted vs. opportunistic auditing, export format, Rule 25/CORLA/BRAVO citations | `auditcenter_analyze-private` design docs, condensed | 1.25 | Drafted |
| 3. Data cleaning & normalization | Heterogeneous export eras, bare rows, contest-name variants, the Excel date-autodetection identifier remapping (unintentional, fully recoverable), manifest mislabeling/gaps and recovery | `CROSS_ELECTION_DB_DESIGN.md`, `DATA_DICTIONARY.md`, `COMPARISON_EXPORTS_CORRUPTED_IN_EXCEL.md` | 3.5 | Drafted |
| 4. Coverage findings | **Purely structural**: targeted / opportunistic / no-record breakdown, county-span breakdown. No risk-value claims. | `scripts/coverage_analysis.py` output | 3 | Drafted |
| 5. Dataset integrity verification | Independent reconstruction of production ballot selections vs. CORLA's own records -- 97.7% exact match, what the 17 mismatches turned out to be | `VALIDATION_RESULTS.md` | 1.5 | Drafted |
| 6. Discrepancies (NEW, added 2026-09-04) | What audits actually found: overall 0.067% genuine-discrepancy rate, SoS reason-category breakdown (Wrong Ballot dominant, 65.6%), Kaplan-Markov type cross-tab, and the discrepancy record's own data-quality gaps (unresolved 20-row reconciliation gap, scope exclusions) | `DISCREPANCY_TYPE_REASON_REPORT.md` | 2.5-3 | Drafted |
| 7. Preliminary conclusions & future work | State open questions plainly as ongoing/future work, without claiming their results: risk-level calculation methodology for opportunistic multi-county contests (with Caron, possibly Stark); CVR-provenance/manual-verification tooling (with Stevens and Raisch) | New writing | 1 | Drafted |

Total: ~13.5-14 pages of budget vs. a 12-page limit -- word count so far
(~7,400 words across all 7 sections) is still comfortably under what this
format typically holds in 12 pages, so likely fine, but confirm with a real
layout pass before trusting the page-budget column above too literally.

## Open items

- [ ] Organizer reply on template + AI-disclosure policy (asked 2026-09-03)
- [ ] Submission web form not yet live -- watch the CFP page
- [ ] Real page-count check once formatted to spec (10pt Times, two-column,
      6.5"x9") -- no template found yet, asked organizers
- [ ] Anonymization pass: every self-citation, repo link, and named
      correspondence needs neutralizing per the double-blind requirement
      (§6 in particular cites `auditcenter`'s own public
      `discrepancy-report-summary.md` by description only, not by name/URL --
      double check nothing in §6 accidentally identifies that repo)
- [ ] A references/bibliography rendering pass -- REFERENCES.md has the
      BibTeX entries, `\cite{}` keys are inline in §2 and §5, but §6 has none
      yet (its content is original empirical work, same as §3 -- confirm
      that's still true, same note as §3's own header comment)
- [ ] Read all seven sections together as one paper, not seven independent
      drafts -- §6 was written after §1-5 and after the outline's own
      section order changed once already (discrepancies inserted as new §6,
      conclusions pushed 6->7); double-check every cross-reference (§ numbers
      inline in the prose) is still correct after any future reordering
