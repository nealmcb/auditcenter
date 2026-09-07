# CORLA data and reproduction package for an EVT/WOTE 2026 submission

This branch packages the public data and code needed to reproduce the
results of an anonymous submission to EVT/WOTE 2026, "Reconstructing,
Cleaning, and Measuring the Coverage of a Decade of Colorado's Public
Risk-Limiting Audit Data." A markdown copy of the paper itself is at
[`paper.md`](paper.md).

## What's here

- **Raw data** (the top-level year directories, `2017/` through `2026/`):
  a mirror of Colorado's own public Audit Center publications --
  per-election ballot manifests, contest parameter files, and
  CVR-vs-audit-board comparison exports, as published by the Colorado
  Department of State based on data exported from the state's
  ColoradoRLA audit software.
- **`cross_election.db`**: the normalized, cross-election SQLite database
  the paper's reconstruction builds from that raw data (§3 of the paper
  describes the cleaning and normalization process in detail). See
  [`DATABASE.md`](DATABASE.md) for its schema and how each table's rows
  trace back to specific files in the raw data above.
- **`corla_results/`**: a Python library that queries `cross_election.db`
  to reproduce every table and headline number in the paper.
- **`reproduce_paper.ipynb`**: a notebook that calls `corla_results` to
  walk through reproducing the paper's findings, section by section.

## Reproducing the paper's results

```
pip install -r requirements.txt
jupyter notebook reproduce_paper.ipynb
```

The notebook reads `cross_election.db` directly; no separate build step
is required to reproduce the paper's tables. Rebuilding that database
from the raw data above (the normalization pipeline itself) is a
separate, larger piece of the underlying project not included in this
submission package.

## Provenance and scope note

This mirror is built by periodically scraping what the Colorado
Secretary of State's Audit Center (and, for some files, individual
counties directly) had published at the time of each scrape -- it is
not a continuous capture of every version of every file. Some files,
ballot manifests in particular, can be revised more than once during an
active audit cycle as errors are found and corrected; if a file changed
between scrapes, this mirror may hold only one snapshot of it, and that
snapshot isn't guaranteed to be the first version, the last version, or
the corrected one. §3.4 of the paper documents a concrete case of this.

The pages this mirror was originally scraped from for elections prior to
the 2026 primary (2017 through 2025) now return 404 on the live
Secretary of State site -- as of 2026-07-13, only the current election's
Audit Center pages are live. The files here for those earlier years
aren't so much stale as orphaned: the original source is simply gone,
and they can no longer be checked against a live copy.

The audit software itself (originally developed under contract with the
Colorado Department of State, now maintained at
[cdos-rla/colorado-rla](https://github.com/cdos-rla/colorado-rla)) and
Colorado's own current Rule 25 (8 CCR 1505-1) governing these audits are
both cited directly in the paper's references.
