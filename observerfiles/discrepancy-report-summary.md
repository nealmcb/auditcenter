# Colorado RLA Discrepancy Reports: Summary 2017–2026

## Data Sources Available

| Election | Report Available |
|---|---|
| 2017 (pilot) | No SOS-annotated discrepancy report found |
| 2018 Primary | No SOS-annotated discrepancy report found; Mineral ballot polling discrepancies in separate docx |
| 2018 General | No SOS-annotated discrepancy report found; Mineral ballot polling discrepancies in separate docx |
| 2019 Coordinated | No SOS-annotated discrepancy report found |
| 2020 Primary | Full annotated SOS PDF |
| 2020 General | Full annotated SOS PDF |
| 2021 Coordinated | Full annotated SOS PDF |
| 2022 Primary | Full annotated SOS PDF |
| 2022 General | SOS-annotated report known to exist (live link in auditCenter Nov 2022) but not yet acquired; not in Wayback Machine |
| 2023 Coordinated | Full annotated SOS PDF (recovered from Wayback Machine, captured 2025-03-02) |
| 2024 General | Full annotated XLSX |
| 2025 Coordinated | Full annotated XLSX |
| 2026 Primary | Full annotated XLSX (also DOCX, same content) |

---

## Elections with Full Annotated Reports (2020–2026)

These elections include the SOS Voting Systems team's classification of each discrepancy reason.

### Category definitions

| Category | Discrepancy bucket |
|---|---|
| **Wrong ballot / Pulled wrong ballot** | Auditing issue |
| **Audit Board Error** | Auditing issue |
| **Voting System Limitation** | Voting system issue (unadjudicated undervote — voter corrected a selection but didn't replace it; system can't discern intent) |
| **Adjudication Error** | Voting system issue (bipartisan judges made an error during tabulation adjudication) |
| **Misconfiguration** | Voting system issue (county misconfigured ballot out-stack conditions; small subset of ballots not queued for human review; 2023 only) |
| **CDOS Instructions Deficiency** | Voting system issue (ClearVote write-in CVR format mismatch, 2022 Primary only) |
| **Duplication Error** | Voting system/process issue (a duplicated ballot's replacement copy — scanned by the voting system in place of a damaged/unreadable original — was not marked to accurately reflect the original's voter intent; the audit board audits the original itself, so this surfaces as an audit discrepancy without being an audit board or wrong-ballot error; 2026 Primary only, per official SoS definition) |
| **Ambiguous Voter Intent** | Human disagreement (audit board and adjudication judges genuinely disagree on hard-to-read marks) |
| **Adjudication Disagreement** | Human disagreement (same phenomenon as Ambiguous Voter Intent; one Broomfield recall case in 2023 labeled differently) |
| **Voter Mistake** | Borderline — voter filled ballot contrary to instructions, making intent unclear |

### Counts by election

| Election | Wrong Ballot | Audit Brd Error | Voting Sys Limit | Adjudication Error | Misconfig | CDOS Deficiency | Duplication Error | Ambiguous Intent | Voter Mistake | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|
| **2020 Primary** | **96** | **16** | 10 | — | — | — | — | — | — | **122** |
| **2020 General** | **185** | **57** | 9 | 23 | — | — | — | 6 | — | **280** |
| **2021 Coordinated** | **6** | **18** | 11 | 4 | — | — | — | 3 | 2 | **44** |
| **2022 Primary** | **52** | **23** | 7 | 2 | — | 4 | — | 2 | 3 | **93** |
| **2023 Coordinated** | **4** | **8** | 1 | — | 2 | — | — | 4 | 3 | **22** |
| **2024 General** | **186** | **34** | 5 | 9 | — | — | — | — | 1 | **235** |
| **2025 Coordinated** | **4** | **11** | 1 | 2 | — | — | — | 4 | — | **22** |
| **2026 Primary** | **6** | **8** | 1 | — | — | — | **1** | — | — | **16** |
| **TOTALS (2020 Primary–2026 Primary, 8 elections)** | **539** | **175** | **45** | **40** | **2** | **4** | **1** | **19** | **9** | **834** |

Totals cover only the 8 elections with full annotated reports above — 2017–2019 and 2022 General have partial/raw, uncategorized data only and are deliberately excluded (see "Elections Without Full Annotated Reports" below), not silently folded in.

Notes on 2023 Coordinated counts: the 4 "Ambiguous Intent" entries include 3 labeled "Ambiguous Voter Intent" (Lake County ballot issues) and 1 labeled "Adjudication Disagreement" (Broomfield recall).

Notes on 2026 Primary counts: parsed from `2026DiscrepancyReportPE.xlsx` (16 data rows; the DOCX version carries the same content plus the category definitions quoted above, including "Duplication Error"'s official text — cross-checked, identical categorization). "Duplication Error" is a genuinely new category, not seen in any prior year's report and not an existing bucket this project invented a fit for — it has its own official SoS definition (see table above) and is used for exactly one entry (Routt County, State Treasurer - REP). This election's own independent CVR-vs-audit-board reproduction (`auditcenter_analyze`'s `discrepancy_verification.py`, in the companion analysis repo) finds the identical 16 rows on 9 distinct ballots, an exact match.

### Cross-cutting patterns

**Auditing issues dominate** in elections with large clusters: a single county pulling the wrong ballot for many ballots creates dozens of discrepancies at once.
- **2020 Primary**: Hinsdale County accounted for ~80 of the 96 "pulled wrong ballot" entries — the entire Hinsdale batch was pulled from the wrong precinct.
- **2020 General**: 185 wrong-ballot entries spread across more counties; Adjudication Error appeared prominently (23) for the first time, reflecting the larger and more complex election.
- **2024 General**: Largest total (235), dominated again by wrong-ballot (186, 79%).

**Voting System Limitation** is a consistent low-level presence in every election (1–11 entries). It represents a structural quirk: when a voter corrects a selection without substituting another, the system's CVR records the corrected-over mark as the vote (to avoid an overvote requiring adjudication). Audit boards reading the physical ballot see a blank; the CVR shows the old mark. This is not fraud, not error — it is an inherent limitation of the optical scan plus adjudication workflow.

**Adjudication Error** is significant when complex ballots or close contests attract many adjudicated ballots. This is a voting system *process* issue: the bipartisan judge team reviewing ambiguous ballots during tabulation applied the Voter Intent Guide incorrectly. Appeared at 23 in 2020 General, 4 in 2021, 2 in 2022, 9 in 2024, 2 in 2025.

**Misconfiguration (2023 Coordinated only)**: Dolores County did not properly configure ballot out-stack conditions, so a small subset of ballots (Proposition HH) were never queued for human adjudication review. 2 entries. A county administration error rather than a voting system or audit board error per se.

**CDOS Instructions Deficiency (2022 Primary only)**: The two ClearVote counties (Garfield, Rio Blanco) encode certified write-ins differently from Democracy Suite; the mitigation instructions from the state were incomplete. 4 entries. Write-in votes were tabulated correctly — only the audit comparison was affected.

**Ambiguous Voter Intent / genuine human disagreement**: The smallest category across all elections. Never more than 6 in any election with a formal report. These are the cases where the audit board and the original adjudication team both looked at the same ballot image and reached different conclusions — reflecting genuinely hard-to-read marks. 2023 Coordinated had 3 Ambiguous Voter Intent entries (Lake County ballot issues) plus 1 "Adjudication Disagreement" (Broomfield recall) — the same phenomenon under a different label. 2025 Coordinated had 4 such entries, all from Clear Creek County (Idaho Springs City Council and Mayor), where the audit board noted "voter intent not clear, per voter intent guide" and marked `consensus: NO`. **2026 Primary had none at all** — the first election in this survey's full-report era with zero entries in this category (and zero Voter Mistake, zero Adjudication Error too); every one of its 16 discrepancies has a mundane auditing or process explanation, not a genuine interpretation dispute.

**2026 Primary**: smallest total of any election with a full annotated report (16, below even 2023's and 2025's 22), dominated by Audit Board Error (8, spread one-per-ballot across 6 counties: Arapahoe, Conejos, Jefferson ×2, Larimer ×3, San Miguel) rather than by Wrong Ballot for once. Its 6 Wrong Ballot entries are all a *single* physical ballot (Broomfield `104-109-47`) mismatching across six different Democratic primary contests — the same single-ballot-multiple-contest pattern as Hinsdale 2020 and Rio Blanco 2022's clusters, just at the scale of one ballot rather than a whole batch or precinct. The companion analysis repo's own independent CVR-vs-audit-board reproduction had flagged this specific ballot as "worth a closer look" (a pattern that read, before this official report existed, more like a possible CVR/ballot-pairing anomaly than an ordinary misread) — this report's own SoS Voting Systems team determination resolves that open question with the mundane explanation: **Wrong Ballot**, i.e. the audit board simply retrieved the wrong physical ballot for that voter. And **Duplication Error makes its first appearance in this survey** (1 entry, Routt County, State Treasurer - REP): the SoS's own new category for when a ballot's *duplicate* — the replacement copy scanned by the tabulator in place of a damaged/unreadable original — wasn't marked to accurately capture the original's voter intent, distinct from both Wrong Ballot (audit board error, not tabulation) and Voting System Limitation (an unrelated, narrower undervote-correction quirk).

---

## Elections Without Full Annotated Reports

### 2017 Pilot (statewide comparison RLA; no SOS-annotated discrepancy report found)

The 2017 pilot was a statewide comparison RLA with ballot-list data for ~60 counties in round_1 and 3 counties in round_2 (Lake, Pueblo, Teller). Six counties (Custer, Douglas, Garfield, Las Animas, Montrose, Rio Blanco) additionally had ballot polling audits. No SOS-annotated discrepancy report has been found.

The only discrepancy detail available in this mirror is an Arapahoe County database export produced by the rla_export tool (at `../2017/arapahoe/`), which shows 3 ballot-level discrepancies:
- Two **City of Aurora Council Member At-Large** ballots where the CVR and audit board agreed on one candidate (Tom Tobiassen) but differed on the second — likely **audit board error**.
- One **City of Centennial Mayor** — completely different candidates (Stephanie Piko vs. C.J. Whelan III) — likely **audit board error or wrong ballot**.

Also notable: Jefferson County had a discrepancy on an unopposed contest (documented in the jeffco-discrepancy-unopposed images), almost certainly a **voting system limitation**.

### 2018 Primary and 2018 General (statewide comparison RLA; no SOS-annotated discrepancy report found)

Both were statewide comparison RLAs. The mirror contains ballot-list data for all counties in round_1 (and round_2 for a subset). The 2018 General additionally has per-county XLSX reports for all counties. Some counties additionally had ballot polling audits; Mineral County's ballot polling discrepancies are documented in the Mineral explanation PDFs in this mirror:

- **2018 Primary (Mineral)**: Two discrepancies — (1) a lightly penciled ballot the scanner failed to read (voting system/hardware limitation); (2) a ballot the tabulator didn't re-feed properly (operator/machine error).
- **2018 General (Mineral)**: One discrepancy — another lightly penciled ballot not picked up by the scanner (voting system/hardware limitation).

No SOS-annotated discrepancy report covering the full comparison RLA has been found for either election.

### 2019 Coordinated (raw contestComparison data, 110 raw discrepancies in round 3; no SOS-annotated report found)

No SOS-annotated discrepancy report has been found for this election; the Wayback Machine CDX shows zero captures for all guessed URL patterns. Raw contestComparison data categorized manually:

| Pattern | Count | Likely cause |
|---|---|---|
| Same candidates, different order | ~56 | **Voting system/software artifact** — CVR records candidates in selection order; audit board reports them in ballot-listed order. A known software issue at the time. |
| Yes/No ballot measure flipped | ~39 | Mix of **audit board error** and possibly **wrong ballot** |
| Genuinely different candidates | ~15 | **Audit board error** or **wrong ballot** |

The ordering discrepancies represent a systematic software design issue, not actual disagreements about votes.

### 2022 General (raw CVR comparison data, 214 raw discrepancies in round 3; no SOS-annotated report found)

A SOS-annotated discrepancy report is known to exist: the auditCenter page carried a live `<a href>` link to `DiscrepancyReport.pdf` during the November 2022 audit period. The file has not been acquired — it is not in the Wayback Machine and currently returns 404 on the SoS site. It should be obtainable by request from the SoS office. Large clusters in Rio Blanco (46), Kiowa (29), Routt (19), Crowley (18) suggest **wrong ballot** events similar to Hinsdale 2020. Not further categorized.

---

## Summary by Discrepancy Type Across All Elections

Counts and percentages below are totals across the 8 elections with full annotated reports (2020 Primary–2026 Primary, 834 discrepancies total — see the TOTALS row above); 2017–2019 and 2022 General are excluded, per the same scoping used throughout this file.

| Type | Count | % of 834 | Frequency (qualitative) | Notes |
|---|---:|---:|---|---|
| **Wrong ballot** (auditing) | 539 | 64.6% | Very common; dominates totals in large elections | Single-county batch errors (Hinsdale 2020, Rio Blanco 2022, etc.) create spikes. Procedural training and workflow issue. |
| **Audit board error** (auditing) | 175 | 21.0% | Consistently present, 10–40% of discrepancies in annotated elections | Audit board entered a different candidate than what the voter marked. |
| **Voting System Limitation** (system) | 45 | 5.4% | Low but present in every annotated election | Structural: uncorrected single-selection undervotes. Not fixable without system redesign. |
| **Adjudication Error** (system process) | 40 | 4.8% | Present in most elections, notable spikes in 2020 G (23) and 2024 G (9) | Bipartisan judge teams applying Voter Intent Guide imperfectly during tabulation. |
| **Ambiguous Voter Intent / Adjudication Disagreement** (genuine disagreement) | 19 | 2.3% | Rare: 0–6 per election | Genuine hard-to-read ballots where reasonable humans disagree. |
| **Voter Mistake** | 9 | 1.1% | Rare: 0–3 per election | Voter marked outside target areas; intent genuinely unclear. |
| **CDOS Instructions Deficiency** (system) | 4 | 0.5% | Once (2022 Primary, 4 entries) | Write-in CVR format mismatch with ClearVote; since addressed. |
| **Misconfiguration** (system/admin) | 2 | 0.2% | Once (2023 Coordinated, 2 entries, Dolores County) | County ballot out-stack misconfiguration prevented human review of some ballots. |
| **Duplication Error** (system/process) | 1 | 0.1% | Once (2026 Primary, 1 entry, Routt County) | A ballot's duplicate copy (made to replace a damaged/unreadable original for scanning) wasn't marked to match the original's voter intent; audit board correctly read the original per protocol. |
| **Total** | **834** | **100.0%** | | |

**The vast majority of discrepancies are auditing-process issues** (wrong ballot retrieved or data entry error) — Wrong Ballot and Audit Board Error together account for **714 of 834 (85.6%)** — not evidence of voting system errors or contested vote interpretation. Genuine human disagreement on voter intent (Ambiguous Voter Intent / Adjudication Disagreement) is rare: 19 of 834 (2.3%), typically 0–6 cases per election statewide.
