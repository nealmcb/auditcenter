# URLs Not Archived by Wayback Machine — Request for Preservation

These are Colorado SoS RLA pages and files confirmed absent from the Wayback Machine
(or not yet verified due to CDX outages), collected so they can be submitted as
save/recover requests to archive.org or other preservation services.

## How these were identified

The Scrapy spider (`auditcenter/spiders/audit_data.py`) was run against each election's
audit page URL (passed via `-a audit_center_url=...`) and crawled all links starting with
`https://www.coloradosos.gov/pubs/elections/RLA`. Files it downloaded are in this mirror.
Files *not* in the mirror were either not linked from those pages, or linked but absent
from the server at crawl time.

The Wayback Machine CDX API (`web.archive.org/cdx/search/cdx`) was queried for all
candidate discrepancy report URLs. Results below reflect CDX status as of 2026-06-06
(note: archive.org was intermittently offline that day; some results are from earlier
successful CDX responses).

**Note:** Before ~2020, the SoS website was at `www.sos.state.co.us` rather than
`www.coloradosos.gov`. Both domain variants are listed where relevant.

---

## Old-format per-election audit pages (from auditCenter dropdown menu)

These pages were live at the time the mirror was built but are now dead (404/redirect).
They are the entry points from which discrepancy reports and other files were linked.
**All confirmed as having zero HTTP-200 captures in Wayback Machine (verified 2026-06-06).**

| URL | CDX status |
|---|---|
| `https://www.coloradosos.gov/pubs/elections/RLA/2017/audit.html` | **0 captures** |
| `https://www.coloradosos.gov/pubs/elections/RLA/2018/primary/audit.html` | **0 captures** |
| `https://www.coloradosos.gov/pubs/elections/RLA/2018/general/audit.html` | **0 captures** |
| `https://www.coloradosos.gov/pubs/elections/RLA/2019/audit.html` | **0 captures** |
| `https://www.coloradosos.gov/pubs/elections/RLA/2020/presidential/audit.html` | not checked |
| `https://www.coloradosos.gov/pubs/elections/RLA/2020/statePrimary/audit.html` | not checked |
| `https://www.coloradosos.gov/pubs/elections/RLA/2020/general/audit.html` | not checked |
| `https://www.coloradosos.gov/pubs/elections/RLA/2021/coordinated/audit.html` | not checked |
| `https://www.coloradosos.gov/pubs/elections/RLA/2022/primary/audit.html` | not checked |

Old domain variants (spider code notes pre-2020 domain was `sos.state.co.us`):
All four checked — **0 captures** for each:

- `https://www.sos.state.co.us/pubs/elections/RLA/2017/audit.html`
- `https://www.sos.state.co.us/pubs/elections/RLA/2018/primary/audit.html`
- `https://www.sos.state.co.us/pubs/elections/RLA/2018/general/audit.html`
- `https://www.sos.state.co.us/pubs/elections/RLA/2019/audit.html`

---

## Missing discrepancy report PDFs

These are the specific discrepancy report files that are absent from the mirror and
were not found as 200-status captures in the Wayback Machine CDX (where verified).

### URL confirmed by an actual link in a scraped HTML page — absent from Wayback Machine

| Election | URL | Source of link | CDX result |
|---|---|---|---|
| 2022 General | `https://www.coloradosos.gov/pubs/elections/RLA/files/2022/general/DiscrepancyReport.pdf` | Live `<a href>` in auditCenter snapshots of 2022-11-22 through 2022-11-24 | 0 captures |

### URLs guessed from the naming pattern of confirmed reports — absent from Wayback Machine

No HTML page in the mirror or on the live SoS site was found to contain a link to these URLs.
They were constructed by analogy with the known URL pattern (`/RLA/<year>/<election>/DiscrepancyReport.pdf`)
and checked in CDX to see if the files had ever existed at these locations.

| Election | URL guessed | CDX result |
|---|---|---|
| 2017 Coordinated | `https://www.coloradosos.gov/pubs/elections/RLA/2017/DiscrepancyReport.pdf` | 0 captures |
| 2017 Coordinated (old domain) | `https://www.sos.state.co.us/pubs/elections/RLA/2017/DiscrepancyReport.pdf` | 0 captures |
| 2018 Primary | `https://www.coloradosos.gov/pubs/elections/RLA/2018/primary/DiscrepancyReport.pdf` | 0 captures |
| 2018 Primary (old domain) | `https://www.sos.state.co.us/pubs/elections/RLA/2018/primary/DiscrepancyReport.pdf` | 0 captures |
| 2018 Primary (alt path) | `https://www.coloradosos.gov/pubs/elections/RLA/files/2018/primary/DiscrepancyReport.pdf` | 0 captures |
| 2018 General | `https://www.coloradosos.gov/pubs/elections/RLA/2018/general/DiscrepancyReport.pdf` | 0 captures |
| 2018 General (old domain) | `https://www.sos.state.co.us/pubs/elections/RLA/2018/general/DiscrepancyReport.pdf` | 0 captures |
| 2018 General (alt path) | `https://www.coloradosos.gov/pubs/elections/RLA/files/2018/general/DiscrepancyReport.pdf` | 0 captures |
| 2019 Coordinated | `https://www.coloradosos.gov/pubs/elections/RLA/2019/DiscrepancyReport.pdf` | 0 captures |
| 2019 Coordinated (old domain) | `https://www.sos.state.co.us/pubs/elections/RLA/2019/DiscrepancyReport.pdf` | 0 captures |
| 2019 Coordinated (alt 1) | `https://www.coloradosos.gov/pubs/elections/RLA/2019/coordinated/DiscrepancyReport.pdf` | 0 captures |
| 2019 Coordinated (alt 2) | `https://www.coloradosos.gov/pubs/elections/RLA/files/2019/coordinated/DiscrepancyReport.pdf` | 0 captures |
| 2020 Presidential Primary | `https://www.coloradosos.gov/pubs/elections/RLA/files/2020/presidential/DiscrepancyReport.pdf` | 0 captures |

Note: the 2020 Presidential Primary audit page in the mirror states Adams County had
"no discrepancies"; it is possible the overall audit had no discrepancies and no report
was generated.

### Found and recovered

| Election | URL | Status |
|---|---|---|
| 2023 Coordinated | `https://coloradosos.gov/pubs/elections/RLA/files/2023/coordinated/DiscrepancyReport.pdf` | **Downloaded** from Wayback capture 20250302112507; saved to `2023/coordinated/DiscrepancyReport.pdf` |

**2026-07-24 bulk recovery:** a systematic Wayback CDX bulk pull and comparison against
this mirror (done in the sibling `auditcenter-wayback` repo; full methodology and
per-year analysis in `auditcenter_analyze-private/output/2026-primary/WAYBACK_COMPARISON_FINDINGS.md`)
found this mirror's spider had never captured the per-county final audit report PDFs,
round CSVs, and manifests for three entire elections -- not just isolated missing
discrepancy reports. All recovered from Wayback captures; per-file source URL + capture
timestamp is in each directory's own `WAYBACK_RECOVERED.md`:

| Election | Files recovered | Manifest |
|---|---:|---|
| 2022 General | 62 | `2022/general/WAYBACK_RECOVERED.md` |
| 2022 Primary | 1 | `2022/primary/WAYBACK_RECOVERED.md` |
| 2023 Coordinated | 120 | `2023/coordinated/WAYBACK_RECOVERED.md` |
| 2024 Presidential Primary | 77 | `2024/presidential/WAYBACK_RECOVERED.md` |
| 2024 Primary | 61 | `2024/primary/WAYBACK_RECOVERED.md` |

Also recovered: `OverviewThreeYearsIn.pdf` (a standalone, non-year-specific RLA program
overview document, from Wayback capture 20201110121126).

Deliberately NOT recovered: narrative/dashboard status pages (`audit.html`,
`riskLimit.html`, `countyManifest.html`, `finalReports.html`, `background.html`,
per-county pages like `Gunnison.html`) and the Spanish FAQ page (`faqsEsp.html`) --
these are consistently absent from this mirror across every year from 2017 through 2024
despite having Wayback captures, which looks like a deliberate original scope decision
(this mirror captures data files, not the SoS's live status-page chrome) rather than a
gap, and their informational value is already covered by the data files recovered above.
Recovery script: `recover_wayback_only_2022_2024.py`.

---

## Notes on 2022 General

The 2022 General discrepancy report link (`/pubs/elections/RLA/files/2022/general/DiscrepancyReport.pdf`)
appeared as a **live href** in the auditCenter page snapshots taken during the audit
(November 22–24, 2022), suggesting it was expected to be published. However:
- The file was never actually uploaded (CDX shows 0 captures with HTTP 200)
- The link was later removed from the auditCenter page
- The live SoS site returns 404 for this URL today

This is the only election where a formal discrepancy report was promised but apparently
never delivered.

---

## How to submit a Wayback Machine save request

For URLs that may have been captured but not indexed, or to request a fresh crawl:
- Save Page Now: `https://web.archive.org/save/`
- Wayback Machine availability API: `https://archive.org/wayback/available?url=<url>`

The script `fetch_missing_discrepancy_reports.py` in this directory can be re-run
once archive.org is stable to attempt automated recovery of any captures found.
