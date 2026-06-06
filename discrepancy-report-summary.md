# Colorado RLA Discrepancy Reports: Summary 2017–2025

## Data Sources Available

| Election | Report Available |
|---|---|
| 2017 (pilot) | Arapahoe raw data only; no SOS-categorized report |
| 2018 Primary | No formal report; ballot polling only (Mineral docx) |
| 2018 General | No formal report; ballot polling Mineral docx only |
| 2019 Coordinated | No formal report; raw contestComparison CSVs |
| 2020 Primary | Full annotated SOS PDF |
| 2020 General | Full annotated SOS PDF |
| 2021 Coordinated | Full annotated SOS PDF |
| 2022 Primary | Full annotated SOS PDF |
| 2022 General | No formal report; raw CVR comparison CSV only (link in auditCenter was a placeholder, never published; not in Wayback Machine) |
| 2023 Coordinated | Full annotated SOS PDF (recovered from Wayback Machine, captured 2025-03-02) |
| 2024 General | Full annotated XLSX |
| 2025 Coordinated | Full annotated XLSX |

---

## Elections with Full Annotated Reports (2020–2025)

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
| **Ambiguous Voter Intent** | Human disagreement (audit board and adjudication judges genuinely disagree on hard-to-read marks) |
| **Adjudication Disagreement** | Human disagreement (same phenomenon as Ambiguous Voter Intent; one Broomfield recall case in 2023 labeled differently) |
| **Voter Mistake** | Borderline — voter filled ballot contrary to instructions, making intent unclear |

### Counts by election

| Election | Wrong Ballot | Audit Brd Error | Voting Sys Limit | Adjudication Error | Misconfig | CDOS Deficiency | Ambiguous Intent | Voter Mistake | **Total** |
|---|---|---|---|---|---|---|---|---|---|
| **2020 Primary** | **96** | **16** | 10 | — | — | — | — | — | **122** |
| **2020 General** | **185** | **57** | 9 | 23 | — | — | 6 | — | **280** |
| **2021 Coordinated** | **6** | **18** | 11 | 4 | — | — | 3 | 2 | **44** |
| **2022 Primary** | **52** | **23** | 7 | 2 | — | 4 | 2 | 3 | **93** |
| **2023 Coordinated** | **4** | **8** | 1 | — | 2 | — | 4 | 3 | **22** |
| **2024 General** | **186** | **34** | 5 | 9 | — | — | — | 1 | **235** |
| **2025 Coordinated** | **4** | **11** | 1 | 2 | — | — | 4 | — | **22** |

Notes on 2023 Coordinated counts: the 4 "Ambiguous Intent" entries include 3 labeled "Ambiguous Voter Intent" (Lake County ballot issues) and 1 labeled "Adjudication Disagreement" (Broomfield recall).

### Cross-cutting patterns

**Auditing issues dominate** in elections with large clusters: a single county pulling the wrong ballot for many ballots creates dozens of discrepancies at once.
- **2020 Primary**: Hinsdale County accounted for ~80 of the 96 "pulled wrong ballot" entries — the entire Hinsdale batch was pulled from the wrong precinct.
- **2020 General**: 185 wrong-ballot entries spread across more counties; Adjudication Error appeared prominently (23) for the first time, reflecting the larger and more complex election.
- **2024 General**: Largest total (235), dominated again by wrong-ballot (186, 79%).

**Voting System Limitation** is a consistent low-level presence in every election (1–11 entries). It represents a structural quirk: when a voter corrects a selection without substituting another, the system's CVR records the corrected-over mark as the vote (to avoid an overvote requiring adjudication). Audit boards reading the physical ballot see a blank; the CVR shows the old mark. This is not fraud, not error — it is an inherent limitation of the optical scan plus adjudication workflow.

**Adjudication Error** is significant when complex ballots or close contests attract many adjudicated ballots. This is a voting system *process* issue: the bipartisan judge team reviewing ambiguous ballots during tabulation applied the Voter Intent Guide incorrectly. Appeared at 23 in 2020 General, 4 in 2021, 2 in 2022, 9 in 2024, 2 in 2025.

**Misconfiguration (2023 Coordinated only)**: Dolores County did not properly configure ballot out-stack conditions, so a small subset of ballots (Proposition HH) were never queued for human adjudication review. 2 entries. A county administration error rather than a voting system or audit board error per se.

**CDOS Instructions Deficiency (2022 Primary only)**: The two ClearVote counties (Garfield, Rio Blanco) encode certified write-ins differently from Democracy Suite; the mitigation instructions from the state were incomplete. 4 entries. Write-in votes were tabulated correctly — only the audit comparison was affected.

**Ambiguous Voter Intent / genuine human disagreement**: The smallest category across all elections. Never more than 6 in any election with a formal report. These are the cases where the audit board and the original adjudication team both looked at the same ballot image and reached different conclusions — reflecting genuinely hard-to-read marks. 2023 Coordinated had 3 Ambiguous Voter Intent entries (Lake County ballot issues) plus 1 "Adjudication Disagreement" (Broomfield recall) — the same phenomenon under a different label. 2025 Coordinated had 4 such entries, all from Clear Creek County (Idaho Springs City Council and Mayor), where the audit board noted "voter intent not clear, per voter intent guide" and marked `consensus: NO`.

---

## Elections Without Full Annotated Reports

### 2017 Pilot (Arapahoe only, raw data)

3 ballot-level discrepancies found in the raw export:
- Two **City of Aurora Council Member At-Large** ballots where the CVR and audit board agreed on one candidate (Tom Tobiassen) but disagreed on the second vote — likely **audit board error** (wrong candidate name recorded).
- One **City of Centennial Mayor** — completely different candidates (Stephanie Piko vs. C.J. Whelan III) — likely **audit board error or wrong ballot**.

No SOS categorization. Also notable: Jefferson County had a discrepancy on an unopposed contest (documented separately in the jeffco-discrepancy-unopposed images), almost certainly a **voting system limitation** (system flagged a non-contested contest).

### 2018 Ballot Polling Audits (Mineral County)

Both the **2018 Primary** and **2018 General** Mineral explanations involve the county's aging 12-year-old optical scanner:
- **2018 Primary**: Two discrepancies — (1) a lightly penciled ballot the scanner failed to read (voting system/hardware limitation); (2) a ballot that the tabulator didn't re-feed properly and the judge didn't catch (operator/machine error, borderline auditing and voting system).
- **2018 General**: One discrepancy — another lightly penciled ballot not picked up by the scanner (voting system/hardware limitation).

Both clearly **voting system issues** (hardware limitations of an old scanner, not ballot manipulation). No formal discrepancy report was published for 2018 or found in the Wayback Machine.

### 2019 Coordinated (raw contestComparison data, 110 raw discrepancies in round 3)

No formal SOS annotation; no discrepancy report found in Wayback Machine. Raw data categorized manually:

| Pattern | Count | Likely cause |
|---|---|---|
| Same candidates, different order | ~56 | **Voting system/software artifact** — CVR records candidates in selection order; audit board reports them in ballot-listed order. A known software issue at the time. |
| Yes/No ballot measure flipped | ~39 | Mix of **audit board error** and possibly **wrong ballot** |
| Genuinely different candidates | ~15 | **Audit board error** or **wrong ballot** |

The ordering discrepancies represent a systematic software design issue, not actual disagreements about votes.

### 2022 General (raw data, 214 raw discrepancies in round 3)

No formal report published (the auditCenter page had a placeholder link during the audit in November 2022, but the file was never made available and is not in the Wayback Machine). Large clusters in Rio Blanco (46), Kiowa (29), Routt (19), Crowley (18) suggest **wrong ballot** events at the county level similar to Hinsdale 2020. Not further categorized.

---

## Summary by Discrepancy Type Across All Elections

| Type | Frequency | Notes |
|---|---|---|
| **Wrong ballot** (auditing) | Very common; dominates totals in large elections | Single-county batch errors (Hinsdale 2020, Rio Blanco 2022, etc.) create spikes. Procedural training and workflow issue. |
| **Audit board error** (auditing) | Consistently present, 10–40% of discrepancies in annotated elections | Audit board entered a different candidate than what the voter marked. |
| **Voting System Limitation** (system) | Low but present in every annotated election | Structural: uncorrected single-selection undervotes. Not fixable without system redesign. |
| **Adjudication Error** (system process) | Present in most elections, notable spikes in 2020 G (23) and 2024 G (9) | Bipartisan judge teams applying Voter Intent Guide imperfectly during tabulation. |
| **Misconfiguration** (system/admin) | Once (2023 Coordinated, 2 entries, Dolores County) | County ballot out-stack misconfiguration prevented human review of some ballots. |
| **CDOS Instructions Deficiency** (system) | Once (2022 Primary, 4 entries) | Write-in CVR format mismatch with ClearVote; since addressed. |
| **Ambiguous Voter Intent / Adjudication Disagreement** (genuine disagreement) | Rare: 0–6 per election | Genuine hard-to-read ballots where reasonable humans disagree. |
| **Voter Mistake** | Rare: 0–3 per election | Voter marked outside target areas; intent genuinely unclear. |

**The vast majority of discrepancies are auditing-process issues** (wrong ballot retrieved or data entry error), not evidence of voting system errors or contested vote interpretation. True human disagreement on voter intent is rare — typically 0–6 cases per election statewide.
