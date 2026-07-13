# 2026 Primary: observer-collected details

Notes on county-provided files collected directly by observers, as a
supplement to the mirrored [Audit Center](../countyManifest.html) data in
[`../files/`](../files/). See [evidence-timestamping.md](../../../evidence-timestamping.md)
for how this evidence gets publicly timestamped.

## Critical finding: La Plata, Morgan, and Saguache manifests are duplicated on the SoS site

As of 2026-07-13 (primary dice-roll day), the Colorado SOS's own live site
serves **byte-identical content** for three different counties' ballot
manifests at:

- `https://www.coloradosos.gov/pubs/elections/RLA/2026/primary/files/LaPlata.csv`
- `https://www.coloradosos.gov/pubs/elections/RLA/2026/primary/files/Morgan.csv`
- `https://www.coloradosos.gov/pubs/elections/RLA/2026/primary/files/Saguache.csv`

All three return the same SHA-256 (`64dec2dc...4366c`), which is Saguache's
actual manifest (1,654 ballot cards, tabulator 102 in 25-card batches).
La Plata's and Morgan's real manifests are nothing like this data — see
below. This means the manifests currently posted for La Plata and Morgan are
simply wrong, not just stale or reformatted.

This was caught by comparing the SoS-posted files against manifests obtained
directly from the counties (below), then confirmed by hashing all 61 posted
manifests and finding this was the only collision — no other counties are
affected.

**Resolved as of 10:20 MDT, 2026-07-13.** Both `LaPlata.csv` and
`Morgan.csv` now serve county-specific data. Morgan's posted file is now
byte-for-byte identical to the county-provided copy below. La Plata's posted
file parses to the same data as the county-provided copy below, differing
only in CSV quoting style (SoS's version leaves fields unquoted; the
county's copy quotes them).

**This looks like a publishing-pipeline issue rather than a county-data
problem.** SoS also posts [`files/uploadStatus.csv`](../files/uploadStatus.csv),
an internal log of county upload activity for the RLA system. It shows both
La Plata's and Morgan's manifests were successfully imported ahead of the
dice roll, so the correct data was already in the system; whatever step
exports that data to the public Audit Center page appears to be what served
Saguache's file under their names instead.

## La Plata County

- County-provided files (via Google Drive, received 2026-07-13):
  - [`LaPlata_BallotManifest.csv`](LaPlata_BallotManifest.csv) — 16,146
    ballot cards, tabulators 102/103, 50-card batches in numbered bins.
    Confirms this is genuinely different data from what SoS posts under
    La Plata's name (see above).
  - [`LaPlata_RedactedTest_NoContestBalance_CVR_Export_20260709081424.csv`](LaPlata_RedactedTest_NoContestBalance_CVR_Export_20260709081424.csv) —
    redacted CVR export from the county, dated 2026-07-09.
- We now have La Plata's manifest confirmed straight from the county itself,
  in addition to (in place of, until SoS fixes the posted file) the Audit
  Center copy.

## Morgan County

- County-provided files (received 2026-07-13):
  - [`Morgan_BallotManifest.csv`](Morgan_BallotManifest.csv) — 5,220 ballot
    cards, tabulator 102, mostly 50-card batches. Also genuinely different
    from what SoS posts under Morgan's name (see above).
  - [`Morgan_CVR_Export_20260709092315_Redacted.csv`](Morgan_CVR_Export_20260709092315_Redacted.csv) —
    redacted CVR export from the county, dated 2026-07-09.
- Same situation as La Plata: manifest confirmed straight from the county,
  supplementing the (currently incorrect) Audit Center copy.

## Weld County

- Files from Teague, received by email at 10:03 MDT on 2026-07-13 — Neal
  attests personally to this receipt time, before the dice roll concluded
  at approximately 10:10:
  - [`Weld_BallotManifest.csv`](Weld_BallotManifest.csv) — byte-for-byte
    identical (SHA-256 `c26253088b...eaeab1b`) to the manifest already
    posted at SoS's `files/Weld.csv`, confirming that one is correct.
  - [`Weld_CVR_Export_20260709140755.csv`](Weld_CVR_Export_20260709140755.csv) —
    redacted CVR export from the county, dated 2026-07-09, converted here
    from the original `.xlsx` for consistency with the other CVR files.
