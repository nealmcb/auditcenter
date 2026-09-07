# EVT/WOTE 2026 case-study paper

Case-study submission to [EVT/WOTE
2026](https://centerforvoting.rice.edu/electronic-voting-technologies-workshop-trustworthy-elections-conference)
(Rice Center for Voting, Dec 7, 2026): reconstructing, cleaning, and
measuring the structural coverage of Colorado's production risk-limiting
audit data, 2017-2026.

## Building the PDF

```
make pdf
```

converts `sections/*.md` into LaTeX (`latex/md2latex.py`) and compiles it
with `tectonic` (a self-contained LaTeX engine -- no system LaTeX install
needed) into `latex/corla_10.pdf`. `make clean` removes generated files.
`make paper-md` regenerates the repository root's `paper.md` (a plain
concatenation of `sections/*.md`, in order).

The organizers do not provide a template. EVT/WOTE's own historical
'10/'11 CFPs pointed submitters at USENIX's classic `usenix.sty`, which
matches the current format spec exactly -- that's what `latex/corla_10.tex`
uses.

## Format requirements

- Max 12 pages (excl. bibliography/appendices), two-column, 10pt Times Roman,
  12pt leading, 6.5"x9" text block
- **Double-blind**: author names/affiliations, identifying acknowledgements,
  and self-citations must all be neutralized before submission
- PDF emailed directly to the organizers -- no web form
- No formal AI-usage policy, but disclosure is recommended; see the
  compiled PDF's own Acknowledgments section

## Scope boundary -- read before adding content

This paper is deliberately narrow. Two adjacent, stronger results are
explicitly **held out** because they need co-authors not yet confirmed:

- Risk-level calculation methodology for opportunistic multi-county
  contests -- a future co-authored piece.
- CVR redaction/provenance/manual-verification tooling -- a separate
  future co-authored piece.

Note: don't call contests with no name-matched export row "zero coverage"
or "unaudited" -- see §4.1's own framing for why that's wrong and what to
say instead.

## Data dependency

The tables and headline numbers in this paper are reproduced from
`cross_election.db` and the `corla_results` Python library, both at the
**root of this repository** (one directory above this one) -- see the
repository root's own `README.md` and `DATABASE.md`, and run
`reproduce_paper.ipynb` from the repository root to regenerate every
table in this paper directly.

## Layout

- `sections/` -- the paper's own section-by-section markdown source
- `latex/` -- the LaTeX build (converter, template, generated output)
- `REFERENCES.md` -- citation list (BibTeX), with rationale notes
- `TODO.md` -- open editorial/content questions, not part of the paper itself
