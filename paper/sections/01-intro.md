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
