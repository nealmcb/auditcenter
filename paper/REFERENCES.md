# References

Verified against real sources (title/authors/venue/year checked, not
recalled from memory) — none of these are placeholders. `[key]` is the
suggested BibTeX citation key; swap in wherever a `[CITATION]` placeholder
appears in `sections/*.md`. Two entries below (marked) are self-citations
under the double-blind rule — cite them exactly like any other reference,
never as "our own prior work" or similar.

Claude: Pull ideas/ material from, and consider referencing my presentations to BEAC:
  /home/srv/voting/audit/corla/talks/beac-2024-09/slides.md
  /home/srv/voting/audit/corla/talks/beac-2026-08/slides.md (Not actually public IIRC)
  and my corla page on neal.mcburnett.org

Perhaps even some of the material from the Lori/Mike team

## Foundational RLA methodology

```bibtex
@article{stark2008conservative,
  author  = {Stark, Philip B.},
  title   = {Conservative Statistical Post-Election Audits},
  journal = {Annals of Applied Statistics},
  volume  = {2},
  number  = {2},
  pages   = {550--581},
  note    = {\url{https://projecteuclid.org/euclid.aoas/1215118528}},
  month   = jun,
  year    = {2008}
}

@inproceedings{stark2010supersimple,
  author    = {Stark, Philip B.},
  title     = {Super-Simple Simultaneous Single-Ballot Risk-Limiting Audits},
  booktitle = {Proceedings of the 2010 Electronic Voting Technology
               Workshop/Workshop on Trustworthy Elections (EVT/WOTE '10)},
  publisher = {USENIX Association},
  note      = {\url{https://www.stat.berkeley.edu/~stark/Preprints/superSimple10.pdf}},
  year      = {2010}
}

@article{stark2012evidence,
  author  = {Stark, Philip B. and Wagner, David A.},
  title   = {Evidence-Based Elections},
  journal = {IEEE Security \& Privacy},
  volume  = {10},
  number  = {5},
  pages   = {33--41},
  note    = {\url{https://www.stat.berkeley.edu/~stark/Preprints/evidenceVote12.pdf}},
  year    = {2012}
}

@article{lindeman2012gentle,
  author  = {Lindeman, Mark and Stark, Philip B.},
  title   = {A Gentle Introduction to Risk-Limiting Audits},
  journal = {IEEE Security \& Privacy},
  volume  = {10},
  number  = {5},
  pages   = {42--49},
  note    = {\url{https://www.stat.berkeley.edu/~stark/Preprints/gentle12.pdf}},
  year    = {2012}
}

@inproceedings{lindeman2012bravo,
  author    = {Lindeman, Mark and Stark, Philip B. and Yates, Vincent S.},
  title     = {{BRAVO}: Ballot-polling Risk-limiting Audits to Verify Outcomes},
  booktitle = {Proceedings of the 2012 Electronic Voting Technology
               Workshop/Workshop on Trustworthy Elections (EVT/WOTE '12)},
  publisher = {USENIX Association},
  note      = {\url{https://www.usenix.org/system/files/conference/evtwote12/evtwote12-final27.pdf}},
  month     = aug,
  year      = {2012}
}

@techreport{rlaworkinggroup2012,
  author      = {{Risk-Limiting Audits Working Group}},
  title       = {Risk-Limiting Post-Election Audits: Why and How},
  institution = {Risk-Limiting Audits Working Group},
  note        = {Executive editor Mark Lindeman; contributing editors
                 include Ronald L. Rivest and Philip B. Stark. Version 1.1.
                 \url{https://www.stat.berkeley.edu/~stark/Preprints/RLAwhitepaper12.pdf}},
  month       = oct,
  year        = {2012}
}

@article{lindeman2013retabulation,
  author  = {Lindeman, Mark and Rivest, Ronald L. and Stark, Philip B.},
  title   = {Machine Retabulation is not Auditing},
  note    = {\url{https://www.stat.berkeley.edu/~stark/Preprints/retabNotAudit13.pdf}},
  year    = {2013}
}

@techreport{nas2018securing,
  author      = {{National Academies of Sciences, Engineering, and Medicine}},
  title       = {Securing the Vote: Protecting American Democracy},
  institution = {The National Academies Press},
  address     = {Washington, DC},
  note        = {\url{https://doi.org/10.17226/25120}},
  year        = {2018}
}

@techreport{nas2023moving,
  author      = {{National Academies of Sciences, Engineering, and Medicine}},
  title       = {Moving to Evidence-Based Elections},
  institution = {The National Academies},
  note        = {\url{https://www.nationalacademies.org/news/2023/03/moving-to-evidence-based-elections}},
  year        = {2023}
}
```

Use `stark2008conservative` and `lindeman2012gentle` for §2's opening
statistical framing (Kaplan-Markov comparison audits generally).
`lindeman2012bravo` is a strong choice for §2's mention of BRAVO/ballot-
polling as the alternative RLA family CORLA does not use — and it's worth
noting explicitly in the text that it comes from this same workshop's own
earlier incarnation, which is a nice, true anchor to the venue.
`rlaworkinggroup2012` backs the SHA-256/Kaplan-Markov selection-method
provenance claim in §2/§3. `lindeman2013retabulation` grounds the
software-independent-evidence framing at the top of §2 (why an audit
compares against independently-read paper rather than re-running the
same tabulation software). `nas2018securing` and `nas2023moving` back
§2's legitimacy-anchor sentence naming the National Academies'
endorsement.

## Directly on-topic prior work (self-citations — cite neutrally, per README's double-blind rule)

```bibtex
@article{lindeman2018nextsteps,
  author  = {Lindeman, Mark and McBurnett, Neal and Ottoboni, Kellie and Stark, Philip B.},
  title   = {Next Steps for the {C}olorado {R}isk-{L}imiting {A}udit ({CORLA}) Program},
  journal = {arXiv preprint arXiv:1803.00698},
  note    = {\url{https://arxiv.org/abs/1803.00698}},
  month   = mar,
  day     = {2},
  year    = {2018}
}

@inproceedings{ottoboni2018suite,
  author    = {Ottoboni, Kellie and Stark, Philip B. and Lindeman, Mark and McBurnett, Neal},
  title     = {Risk-Limiting Audits by Stratified Union-Intersection Tests of Elections ({SUITE})},
  booktitle = {International Joint Conference on Electronic Voting (E-Vote-ID)},
  note      = {arXiv:1809.04235, \url{https://arxiv.org/abs/1809.04235}},
  month     = sep,
  day       = {12},
  year      = {2018}
}
```

`lindeman2018nextsteps` is the direct predecessor of this paper's subject:
it identified, in 2018, that Colorado's audits were "restricted to
single-county contests" and proposed methods for multi-county and
combined-audit-type handling — exactly the domain-shape question this
paper's §2/§4 describe as since resolved in production. Cite it in §2 when
introducing multi-county domain shapes, and again in §6 as the direct
ancestor of the still-open opportunistic-risk-methodology question. **Do
not** phrase either citation as "in previous work" in a way that reveals
authorship — just cite the paper like any other (e.g., "Lindeman et
al. [lindeman2018nextsteps] identified the need for..."). `ottoboni2018suite`
is optional background for §2 if a stratified-sampling mention is wanted,
but isn't load-bearing for this paper's actual claims — include only if it
earns its place.

One more citation sits here for convenience even though it is *not* a
self-citation (Rivest, not Neal):

```bibtex
@article{rivest2018consistent,
  author  = {Rivest, Ronald L.},
  title   = {Consistent Sampling with Replacement},
  journal = {arXiv preprint arXiv:1808.10016},
  note    = {\url{https://arxiv.org/abs/1808.10016}},
  month   = aug,
  day     = {29},
  year    = {2018}
}
```

`rivest2018consistent` backs §7's brief, detail-free mention of consistent
sampling as a well-motivated future upgrade path. This citation is safe on
its own terms -- it's Rivest's own published method paper, standing apart
from any of the unpublished cross-domain-independence investigation that's
out of scope for this paper (see "Not included, and why" below). Do not
let this citation become a hook for adding detail about *why* independence
matters here beyond what §7 already says -- that line was deliberately

Another citation sits here for the same section, backing §7's mention of
style-based sampling:

```bibtex
@article{glazer2021style,
  author  = {Glazer, Amanda K. and Spertus, Jacob V. and Stark, Philip B.},
  title   = {More Style, Less Work: Card-style Data Decrease
             Risk-limiting Audit Sample Sizes},
  journal = {Digital Threats: Research and Practice},
  volume  = {2},
  number  = {4},
  pages   = {32},
  note    = {\url{https://dl.acm.org/doi/10.1145/3457907}},
  month   = oct,
  year    = {2021}
}
```
kept generic per Neal's explicit instruction.

## Regulatory and software sources

```bibtex
@techreport{corstatute,
  author       = {{State of Colorado}},
  title        = {Colorado Revised Statutes {\S} 1-7-515: Risk-limiting audits -- rules -- legislative declaration -- definitions},
  howpublished = {\url{https://law.justia.com/codes/colorado/title-1/general-primary-recall-and-congressional-vacancy-elections/article-7/part-5/section-1-7-515/}},
  note         = {The statutory requirement Rule 25 implements},
  year         = {2026}
}

@misc{corules2026,
  author       = {{Colorado Secretary of State}},
  title        = {Election Rules, 8 {CCR} 1505-1, Rule 25 (Risk-Limiting Audits)},
  howpublished = {\url{https://www.coloradosos.gov/pubs/rule_making/CurrentRules/8CCR1505-1/ElectionRules.pdf}},
  year         = {2026}
}

@misc{corlasoftware,
  author       = {{Colorado Department of State}},
  title        = {{CORLA} (Colorado Risk-Limiting Audit Tool) source code},
  howpublished = {\url{https://github.com/cdos-rla/colorado-rla}},
  note         = {Linked directly from the Colorado Secretary of State's
                  own Audit Center page as the current software repository},
  year         = {2026}
}
```

`corstatute` is the actual legal requirement (Rule 25 is the Secretary of
State's implementing regulation, not the underlying law) -- cite both
together for the "mandatory, statewide" claim. `corules2026` backs the
Rule 25 / seed-ceremony description in §2.
`corlasoftware` backs every "confirmed by direct reading of its published
source code" claim in §2/§3 — cite it the first time that phrase appears.

## Not included, and why

- **Anything from the unpublished cross-domain-independence investigation
  itself** (RFC 2777, `cryptorandom`, Rivest's `sampler.py`, any specific
  numbers/examples about which contest pairs are affected or by how much)
  — that entire line of work is a separate, distinct, not-yet-public
  project and out of scope for this paper; don't pull citations from it
  in even for background color, since it would invite the exact detailed
  question §7's deliberately generic mention is not trying to answer.
  **Exception, added 2026-09-04 per Neal**: `rivest2018consistent` (above,
  in "Directly on-topic prior work") is now cited — it's Rivest's own
  independently published method paper, not part of the unpublished
  investigation, and citing it doesn't require explaining *why* it matters
  here beyond the one generic sentence already in §7.
- **Ottoboni & Stark's PRNG-pitfalls paper** — same reason as the
  unpublished-investigation bullet above; still excluded.
- **Anything specifically about the opportunistic risk-calculation
  methodology or CVR-provenance/redaction tooling** — those are the two
  held-out threads (README's "Scope boundary"); don't cite supporting
  literature for either here, since doing so would start making an
  argument this paper isn't making.
