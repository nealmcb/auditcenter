# EVT/WOTE 2026 case-study paper

Working repo for a solo-authored case-study submission to [EVT/WOTE
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

The organizers don't provide a template (see below), but EVT/WOTE's own
historical '10/'11 CFPs pointed submitters at USENIX's classic
`usenix.sty`, which matches the current format spec exactly -- that's
what `latex/corla_10.tex` uses.

## Deadlines

- Paper submission: September 7, 2026, 11:59pm Central
- Acceptance notification: September 30, 2026
- Final camera-ready: October 31, 2026
- Workshop: December 7, 2026, Kraft Hall 130, Rice University

## Format requirements

- Max 12 pages (excl. bibliography/appendices), two-column, 10pt Times Roman,
  12pt leading, 6.5"x9" text block
- **Double-blind**: author names/affiliations, identifying acknowledgements,
  and self-citations must all be neutralized before submission
- PDF emailed directly to `evtwote@rice.edu` -- no web form, and the
  organizers don't provide a template, confirmed by the organizer (Phil
  Kortum) 2026-09-05, see `correspondence/2026-09-03-organizer-email.md`
  -- see "Building the PDF" above for the one this repo uses instead
- No formal AI-usage policy, but disclosure is recommended (same reply)
  -- plan to include a brief disclosure statement in the submission

## Scope boundary -- read before adding content

This paper is deliberately narrow. Two adjacent, stronger results are
explicitly **held out** because they need co-authors who haven't been asked
yet, and there's no time to coordinate that before Sept 7:

- **Risk-level calculation methodology for opportunistic multi-county
  contests** -- belongs to John Caron (and possibly Philip Stark) as a
  future co-authored piece.
- **CVR redaction/provenance/manual-verification tooling** -- belongs to
  Lori Stevens and Mike Raisch as a future co-authored piece.

Note: don't call
contests with no name-matched export row "zero coverage" or "unaudited" --
see the docstring in `scripts/coverage_analysis.py` for why that's wrong and
what to say instead.

## Data dependency

Reads `output/cross_election.db` from the sibling
`auditcenter_analyze-private` repo (`../auditcenter_analyze-private/`) --
not copied in here, it's 800+MB of derived data owned by that project. See
`scripts/coverage_analysis.py --help`.

## Layout

- `OUTLINE.md` -- current section-by-section plan and page budget
- `scripts/` -- analysis scripts producing tables/numbers for the paper
- `correspondence/` -- organizer emails and other paper-logistics correspondence
