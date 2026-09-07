# `cross_election.db`: schema and provenance

A single SQLite database normalizing fourteen Colorado election
instances' worth of CORLA audit exports (2017 through the 2026 primary)
into one relational schema, as described in §3 of the paper. Every row
that originated in a specific raw file carries a `source_file` column
(and, for several tables, a `raw_row` column with the original CSV row
verbatim) pointing back to a specific file under the year directories in
this same repository -- so any number in the paper can be traced back to
the literal published record it came from.

## Tables

- **`elections`** -- one row per election instance (`key`, e.g.
  `"2024-general"`; `export_era`: `ballot_list` (2017/2018-primary/early
  2018-general rounds), `contest_csv` (2019 onward), or `irv` (the
  2025-irv RAIRE-based export, out of scope for this paper -- §3.1)).
- **`counties`** -- Colorado's 64 counties, keyed by a normalized name.
- **`county_manifests`** / **`manifest_batches`** -- each county's own
  ballot manifest for each election: a total ballot count per county,
  and (where available) the individual tabulator/batch records within
  it, each with `start_position`/`end_position` giving that batch's
  1-indexed range within that county's own manifest (local to the
  county, not a cross-county global numbering).
- **`true_contests`** -- one row per real contest per election, after
  the fragment-consolidation described in §3.2. `coverage_status` is
  `'targeted'`, `'opportunistic_covered'`, `'fragmented_only'`, or
  `'zero_coverage'` (Table 1's classification, §4.1).
- **`contest_fragments`** -- the raw, pre-consolidation contest rows as
  CORLA's own export named them (one true contest can have several
  fragments -- a bare row plus county-suffixed forced fragments), each
  carrying that fragment's own reported `audited_sample_count` and
  Kaplan-Markov aggregate counts.
- **`contest_counties`** -- which counties each true contest's own
  ballot population spans (used for Table 1's single/partial/statewide
  classification).
- **`contest_selection_rows`** -- CORLA's own recorded selection
  (`contest_cvr_ids`, a JSON list of the audit software's internal CVR
  identifiers) for each contest's formal targeted draw, by round.
- **`ballot_comparisons`** -- one row per examined ballot-contest pair:
  the voting system's own recorded choice, the audit board's hand
  interpretation, and (precomputed at import time) `is_genuine_discrepancy`
  and `discrepancy_type` (`'o2'`/`'o1'`/`'u1'`/`'u2'`/`NULL` -- §6).
- **`audit_random_seeds`** -- the publicly announced random seed for
  each election/round, and the file it was published in.
- **`sos_discrepancy_report_rows`** -- the Secretary of State's own
  separately published post-audit discrepancy report, where one exists,
  with each row's human-assigned reason category (§6.3-6.4).
- **`risk_calculations`** / **`vote_totals`** / **`legacy_county_round_summary`**
  -- CORLA's own reported per-contest risk-calculation inputs/outputs and
  vote totals; not used by the paper's own published results but
  retained for completeness.

## What `corla_results` reads from this database

See `corla_results/coverage.py`, `discrepancies.py`, and
`verification.py` for exactly which tables and columns back each of the
paper's Tables 1 through 5, and `DATABASE.md`'s own accuracy is checked
directly by `reproduce_paper.ipynb`, which reruns every one of those
queries and prints the result next to the paper's own published numbers.
