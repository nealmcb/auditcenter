# Timestamping audit evidence: why, and how we do it

This document explains, for people new to risk-limiting audits (RLAs) and to
cryptographic timestamping alike, why audit evidence gets a public,
independently-verifiable timestamp, how you can check that yourself on Mac,
Windows, or Linux, and how it's produced in this repo. That evidence starts
with the ballot manifests and the target contest list in directories like
[`2026/general/files/`](../2026/general/files/), and extends to redacted cast
vote records (CVRs) from counties that publish them, first piloted in the
2026 primary.
See the [README](../README.md) for background on the data itself, and
[The Colorado Risk-Limiting Audit Project (CORLA) and related work](http://bcn.boulder.co.us/~neal/elections/corla/)
for background on Colorado's RLA process generally.

**Just want to check the evidence yourself?** Skip straight to
["How to verify this yourself, on Mac, Windows, or Linux"](#how-to-verify-this-yourself-on-mac-windows-or-linux)
below. The background and how-we-built-it details follow after that.

*This explanation and tips on verification are no longer quite
hot-off-the-presses: the approach was first used for the 2026 primary, and
is being refined for the 2026 general. It's still a bit clunky (three different
tools, each with its own website and vocabulary, is a lot to ask of someone
who just wants to know "is this real?"). We're actively working on simpler,
easier-to-trust ways to do this. Please send feedback to
[Neal McBurnett](mailto:nealmcb@gmail.com) (nealmcb@gmail.com) or
[open a GitHub issue](https://github.com/nealmcb/auditcenter/issues) on
this repo.*

## Why this matters: the "dice roll" and commitment

A risk-limiting audit starts with a public **random seed generation ceremony**
— the "dice roll" — where members of the public roll fancy ten-sided dice to produce
a random seed. That seed drives the
[pseudo-random number generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator)
that selects which ballots get pulled for hand audit.

The whole point of rolling real dice in public is that nobody, including
election officials, can predict or influence which ballots will be selected.
But that guarantee only holds if the **ballot manifests** (the county-by-county
inventories of how many ballots exist in each batch, which the sampling
algorithm draws against) are locked in *before* the seed exists. If a manifest
could still be edited after the seed is public, someone could in principle
work backwards from the seed to figure out which specific ballots would be
picked, and adjust the manifest (or worse) accordingly. Even without any bad
intent, if there's no public proof of *when* the manifest was locked in, a
skeptical observer has no way to rule that scenario out.

So we need a way to publicly and irrevocably prove: *"this exact set of
bytes existed, unchanged, at this exact time — before the dice were rolled."*
That's a [**cryptographic commitment**](https://en.wikipedia.org/wiki/Commitment_scheme),
and the goal is to make it verifiable
by an ordinary member of the public, not just by people who trust us.

The same reasoning extends beyond manifests to other audit evidence, such as
redacted CVRs (cast vote records): the value of the audit depends on being
able to prove that the evidence being compared against hand counts is the
same evidence that existed at the time it mattered, not something quietly
adjusted afterward to make discrepancies disappear.

Older approaches we've used or considered — posting a hash on Twitter,
commercial timestamping/"stamper" services, various blockchain-notarization
products — each have a weakness: Twitter is no longer reliably archivable or
even machine-readable; commercial timestamping authorities require trusting a
single company; many blockchain-notarization products are themselves
centralized services wrapping a chain underneath, so you're trusting their
server as much as the chain. None of them make independent, tool-free
verification easy for a non-expert.

## What we timestamp, and when

In this archive, a file is **timestamped** when its SHA-256 hash is listed
in a `SHA256SUMS` file that has both an OpenTimestamps proof and a Sigstore
signature, as described below. A git commit on its own is not a timestamp:
commits record what changed in this repository, but their dates are set by
whoever makes them.

The main purpose is to fix the data the audit depends on before the dice
roll. Each election gets only a few timestamps, at the points that matter
to the audit:

- **Before the dice roll:** the ballot manifests, the target contest list,
  the redacted CVRs available by then, and the other files the random
  selection depends on.
- **After the first statewide random selection we reproduce:** the Audit
  Center's upload status and the other files showing that the selection
  was made from the same manifests as the state's RLA software used.
- **When the audit closes:** the county audit reports, discrepancy reports
  and final results.

A `SHA256SUMS` file lists only files that shouldn't change later, so its
checks should keep working unless there's an unusual change. Web pages are mirrored whenever
their content changes, but are not listed. Everything else the observers'
tool recorded is covered by its event log, whose state each `SHA256SUMS`
file names in its header (see
["For the technically inclined: the event log"](#for-the-technically-inclined-the-event-log)
below).

## How to verify this yourself, on Mac, Windows, or Linux

Checking takes two steps. First, check that the file's hash matches the
one recorded in a hash list. Then check when that hash list existed: we
timestamp each hash list through two independent public systems, so you
only need *one* of them — pick whichever is easiest for you. Here's a
concrete example: confirming that Weld County's redacted
cast-vote record for the 2026 Primary
[`observerfiles/Weld_CVR_Export_20260709140755.csv`](../2026/primary/observerfiles/Weld_CVR_Export_20260709140755.csv)
is the exact file we timestamped before the dice roll, not something swapped in afterward.

The terminal commands below are run from the
[`2026/primary/`](../2026/primary/) folder of a copy of this repository.

**First, find the file's recorded hash.** Every `SHA256SUMS*.txt` file lists
one line per evidence file. Open [`2026/primary/observerfiles/SHA256SUMS.v4.txt`](../2026/primary/observerfiles/SHA256SUMS.v4.txt)
(in a text editor, or on GitHub) and find the line for the file you care
about:

```
56d1c5ba446f7f89309304fbe6d73f7e8514e624930111fa5f2965fe26f44241  observerfiles/Weld_CVR_Export_20260709140755.csv
```

### 1. Check the file hash matches

- **No install, any platform**: go to
  [emn178's SHA256 File Checksum tool](https://emn178.github.io/online-tools/sha256_checksum.html)
  and drag `observerfiles/Weld_CVR_Export_20260709140755.csv` onto the drop
  zone. The hash appears immediately — it computes entirely in your browser
  ("process locally and won't be uploaded," per the page itself), no button
  presses or setup required. It's a small personal project rather than an
  institutional one, so if you'd rather use something more established:
  [CyberChef](https://gchq.github.io/CyberChef/) (published by
  [GCHQ](https://en.wikipedia.org/wiki/GCHQ), the UK's signals-intelligence
  agency — roughly the British counterpart to the NSA — but genuinely
  open-source and browser-only) does the same thing, just with more clicks:
  type "SHA2" into its search box (it's not shown by default), drag the
  result into the "Recipe" panel, set it to `256`, then drag your file onto
  the input panel.
- **Or, if you're comfortable with a terminal:**
  - Mac: `shasum -a 256 observerfiles/Weld_CVR_Export_20260709140755.csv` (built in, no install)
  - Windows: `certutil -hashfile observerfiles\Weld_CVR_Export_20260709140755.csv SHA256` (built in, no install) — or, in PowerShell, `Get-FileHash -Algorithm SHA256 .\observerfiles\Weld_CVR_Export_20260709140755.csv`
  - Linux: `sha256sum observerfiles/Weld_CVR_Export_20260709140755.csv`

Compare the output to the hash on the `SHA256SUMS.v4.txt` line above — they
should match exactly.

### 2. Check the OpenTimestamps (Bitcoin-anchored) proof

This proves `SHA256SUMS.v4.txt` itself — and therefore every file it lists —
existed at or before a specific Bitcoin block.

- **No install, any platform**: go to [opentimestamps.org](https://opentimestamps.org/)
  and drag in both [`SHA256SUMS.v4.txt`](../2026/primary/observerfiles/SHA256SUMS.v4.txt) and
  [`SHA256SUMS.v4.txt.ots`](../2026/primary/observerfiles/SHA256SUMS.v4.txt.ots) — it verifies
  the Bitcoin anchor in your browser.
- **Or, if you're comfortable with a terminal:** `pip install opentimestamps-client`
  (Python and pip both have native Mac and Windows installers), then:
  ```
  $ ots --no-bitcoin verify observerfiles/SHA256SUMS.v4.txt.ots
  ```
  This prints the Bitcoin block (957882) and the Merkle root that block must
  have, to compare with any block explorer. With a Bitcoin node of your own,
  `ots verify` without `--no-bitcoin` checks the block itself.

### 3. Check the Sigstore/Rekor transparency-log entry

This proves someone published that same hash to a public, tamper-evident log
at a specific time, independent of Bitcoin or GitHub.

- **No install, any platform**: go to [search.sigstore.dev](https://search.sigstore.dev/)
  and search for the SHA-256 of `SHA256SUMS.v4.txt` itself (not a line inside
  it): `9732f2f9130e8849ad919716cafc96d598b389a91ce504b8fb8742177fcc22ce`. It
  shows you the public log entry directly in your browser.
- **Or, if you're comfortable with a terminal:**
  - Mac: `brew install cosign`
  - Windows: `choco install cosign`, or download the `.exe` from the
    [cosign releases page](https://github.com/sigstore/cosign/releases)
  - Linux: see your package manager, or the same releases page
  - Then, on any platform, with the public key the 2026 primary's files were
    signed with, [`cosign.pub`](../2026/primary/observerfiles/cosign.pub):
    ```
    $ cosign verify-blob --key observerfiles/cosign.pub \
        --bundle observerfiles/SHA256SUMS.v4.txt.cosign-bundle observerfiles/SHA256SUMS.v4.txt
    ```

If the hash check passes, and either of the two timestamp checks passes,
you've independently confirmed the evidence wasn't altered after it was
timestamped — without needing to trust us, GitHub, or any single
calendar/log operator.

**Moved or replaced files.** Sometimes a file isn't where a hash list says,
or its hash doesn't match. That's because occasionally files in this archive
are moved to another folder, or replaced by a later version, after a hash
list naming them was made. That can be resolved safely because a hash identifies a file's content, not
its location. The file is still in this repository, either in another
folder of the same election or as an earlier version. To find it, look
through the election's other folders, or open the file on GitHub and use
its "History" button, which lists every earlier version for viewing and
download. Then check its hash as above. (With a copy of the repository,
`git log --follow -- PATH` lists the same history.)

## Why three separate layers

Each layer has distinct advantages, and providing all three together
means an observer gets the benefits of each:

- **Git commit + public GitHub push**: simple and gives anyone a durable
  public copy, but a commit date is self-reported by whoever makes it, so a
  commit is not a timestamp on its own.
- **Sigstore/Rekor**: a public, append-only transparency log (the same idea
  as Google's Certificate Transparency project, generalized via Google's
  Trillian log server) — entries can't be quietly removed or altered without
  it being detectable. An entry is made within seconds of signing.
- **OpenTimestamps**: anchored to the Bitcoin blockchain. The Bitcoin anchor
  follows quickly, allowing anyone to check the time against a public record
  that no single organization keeps.

## What each check relies on

Two kinds of trust are involved, and they're worth keeping apart:

- **Websites and services that make checking easy.** opentimestamps.org,
  search.sigstore.dev and the online hash tools are run by organizations or
  individuals. If one changes or goes away, the same checks can be made with
  the command-line tools or another site: the proof files in this archive
  don't depend on any of them.
- **The public records that hold the time.** An OpenTimestamps proof is
  self-contained: checking it needs only Bitcoin's record of past blocks,
  not the calendar servers that helped make it. A `.cosign-bundle` holds the
  signed Rekor entry, so it too can be checked from the file alone, with
  Sigstore's published keys; the public log lets anyone look the entry up.

## How these proofs are generated

This section is about *producing* new timestamps — e.g. if you want to
independently stamp your own copy of the evidence to cross-check ours. You
don't need any of this just to verify what's already here; see the section
above for that.

We compute [SHA-256](https://en.wikipedia.org/wiki/SHA-2) hashes of every
evidence file into a single `SHA256SUMS.txt`, commit that alongside the
files themselves to this repo, and push to the public mirror at
[github.com/nealmcb/auditcenter](https://github.com/nealmcb/auditcenter).

For the OpenTimestamps proof, we use the
[`ots`](https://github.com/opentimestamps/opentimestamps-client) client
(`pip install opentimestamps-client` — same install on Mac, Windows, and
Linux):

```
$ ots stamp SHA256SUMS.txt
```

This produces `SHA256SUMS.txt.ots`. Right after stamping, the proof is
"pending" — the calendar servers (independent operators who each batch many
people's hashes into one [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree)
and periodically commit the root into a real Bitcoin transaction) have your
hash queued, and it usually appears on-chain within minutes to an hour. Check
status any time with `ots verify SHA256SUMS.txt.ots`, or `ots upgrade
SHA256SUMS.txt.ots` to fetch and embed a completed proof once a calendar has
confirmed it.

For the Rekor entry, we sign the same file and submit it with
[`cosign`](https://github.com/sigstore/cosign) (`brew install cosign` on
Mac, `choco install cosign` or the `.exe` release on Windows):

```
$ cosign sign-blob --bundle SHA256SUMS.txt.cosign-bundle SHA256SUMS.txt
```

This returns a Rekor **log index** (a public entry number) within seconds.

**Who signed.** The 2026 primary's signatures were made with a
freshly-generated key file, not tied to any verified identity: they show
that one signer logged each entry, not who. From the 2026 general on,
signatures are "keyless": Sigstore binds each one to the signer's verified
login, named in the certificate inside the `.cosign-bundle` file and in the
public Rekor entry. The 2026 general's are signed by `nealmcb@gmail.com`,
verified by Google, and are checked with:

```
$ cosign verify-blob --bundle FILE.cosign-bundle \
    --certificate-identity nealmcb@gmail.com \
    --certificate-oidc-issuer https://accounts.google.com FILE
```

## Random selection example: 2026 primary dice roll

We also want to be able to reproduce the way the random seed
and published manifest data is used to identify exactly which
ballots are selected in each county.

For the 2026 primary dice roll, the concrete artifacts are in
[`2026/primary/`](../2026/primary/):

- [`files/`](../2026/primary/files/) — county manifest CSVs collected from
  Colorado's Audit Center (San Juan County hand-counts and is excluded from
  the audit entirely)
- [`observerfiles/`](../2026/primary/observerfiles/) — manifests and redacted
  CVRs obtained directly from counties;
  [`2026-primary-details.md`](../2026/primary/observerfiles/2026-primary-details.md),
  notes on what was found and confirmed for this election; the text of the
  election's tweet; and the `SHA256SUMS*.txt` files (+ matching `.ots` /
  `.cosign-bundle`), SHA-256 digests of the evidence files above, timestamped
  as described above. Their paths are relative to `2026/primary/`.

We never overwrite a `SHA256SUMS*.txt` once it's been stamped and pushed —
each update to the evidence set gets a new version (`SHA256SUMS.txt`,
`SHA256SUMS.v2.txt`, ...) with its own OTS and Rekor proof, so every
commitment we ever made stays independently checkable, even after later
files supersede it. From the 2026 general on, each is named for its version
and the time it was written, in UTC: `SHA256SUMS-v1-20261106T203137Z.txt`.
The time in the name is the writer's own clock; the proof of time is the
OpenTimestamps and Rekor entries.

This first pilot run had some last-minute churn — a few counties' manifests
weren't posted yet at roll time, one publishing bug briefly served the wrong
county's data, and evidence trickled in from observers throughout the
morning with inconsequential changes in batch numbers,
hence four versions instead of one. `SHA256SUMS.v4.txt` is the
cleanest, most complete snapshot from this run; future elections should need
far fewer versions as the process matures.

### Predicting the first ballot drawn

Once the random seed exists, anyone can predict exactly which ballot a
single-county contest will draw first, using the timestamped manifest and
the same SHA-256 PRNG Colorado's RLA software uses:
`SHA256(seed + "," + i)`, taken as a big integer, mod the county's total
ballot count, plus 1. Colorado
currently samples against each county's *full* manifest — there's no
ballot-style/card-style restriction yet — so this prediction holds for any
single-county contest in that county.

For the 2026 primary seed (established at the July 13 dice roll,
`49006417086137856424`), the first ballot each of these counties would
yield:

| County | Total ballots | Pick # | Ballot (tabulator-batch-position) |
|---|---|---|---|
| La Plata | 16,146 | 7,210 | `102-62-10` |
| Morgan | 5,220 | 1,612 | `102-34-27` |
| Weld | 69,640 | 38,412 | `103-70-1` |

"Pick #" is this ballot's position in the county's own manifest sequence —
not its position in a physical list. The ballot it identifies (e.g.
`102-62-10` for La Plata) will show up somewhere in that county's
imprinted-id pull list once the audit runs, but almost certainly not first
in that list — the pull list is sorted according to the locations where the
boxes of ballots are stored, not by pick number.

These were computed two independent ways — a from-scratch script and
`RLAAuditHelper.py`, from
[loriinboulder](https://github.com/loriinboulder)'s
[`AuditVerificationAssistant`](https://github.com/loriinboulder/AuditVerificationAssistant)
— and matched exactly.

Note this is the single-county prediction, not the statewide one: the
statewide comparison audit (e.g. this primary's U.S. Senate contest, audited
in all 63 counties) draws from a single combined pool of all counties'
ballots together. There's no separate statewide pull list — whichever
county a statewide pick lands in, it just becomes an additional entry in
that county's own pull list, mixed in with its local-contest picks. In a
reference run of the first 118 statewide picks, the very first landed in
Jefferson County, and La Plata and Morgan didn't get a hit at all in that
initial batch (both are small counties relative to the statewide total, so
that's expected, not a red flag).

## 2026 general

The 2026 general's Audit Center files are where this mirror keeps every
Audit Center file, at the paths the Audit Center publishes them: the target
contest list, for example, is
[`2026/general/files/2026GeneralRLAContestList.xlsx`](../2026/general/files/2026GeneralRLAContestList.xlsx).
The observers' evidence is in
[`2026/general/observerfiles/`](../2026/general/observerfiles/): each
`SHA256SUMS-v*.txt` file, with its `.ots` proof and `.cosign-bundle`
signature, and the observers' event log,
[`events.jsonl`](../2026/general/observerfiles/events.jsonl), whose head at
the time each SUMS file names in its header. The first two SUMS files also
list four Audit Center pages; later ones list only files that shouldn't
change.

The first two SUMS files list their files by paths from before the files
were moved to where the mirror keeps them (see "Moved or replaced files"
above), so check each file's hash directly. For the target contest list,
from the `2026/general/` folder:

```
$ sha256sum files/2026GeneralRLAContestList.xlsx
880cc6b89dd8145806332c780f52f4bdd090773e2b2dea9d58420ae8df1b1e0e  files/2026GeneralRLAContestList.xlsx
$ grep 2026GeneralRLAContestList observerfiles/SHA256SUMS-v2-20261107T002551Z.txt
880cc6b89dd8145806332c780f52f4bdd090773e2b2dea9d58420ae8df1b1e0e  auditcenter/2026/general/files/2026GeneralRLAContestList.xlsx
$ ots --no-bitcoin verify observerfiles/SHA256SUMS-v2-20261107T002551Z.txt.ots
$ cosign verify-blob --bundle observerfiles/SHA256SUMS-v2-20261107T002551Z.txt.cosign-bundle \
    --certificate-identity nealmcb@gmail.com \
    --certificate-oidc-issuer https://accounts.google.com observerfiles/SHA256SUMS-v2-20261107T002551Z.txt
```

The OpenTimestamps proof is in Bitcoin block 974874: the target contest
list existed, with that content, by that block, mined at 6:30 PM MST on
6 November 2026. From the next SUMS file on, the paths are relative to the
`2026/general/` folder, and its header's `check:` line checks every file at
once from there:

```
$ sha256sum --check observerfiles/SHA256SUMS-v3-….txt
```

## For the technically inclined: the event log

The observers' tool, [corla-observer](https://github.com/nealmcb/corla-observer),
records everything it does in an append-only event log,
[`events.jsonl`](../2026/general/observerfiles/events.jsonl), published
beside the SUMS files. Each event carries the SHA-256 hash of the one
before it, so the hash of the latest event, the log's "head", depends on
every event up to it. Each SUMS file names the head at the time it was
written, in a header line such as:

```
# event-log-head: 58 dc7f87f60f326d3fdfed407a8480a8c28638eb9c006ac3f3ce900fa251034e6c
```

Because the SUMS file is timestamped, so is that head, and with it every
event up to event 58. Events that record a file carry the file's SHA-256 in
their `file_sha256` field: each fetch from the Audit Center, for example.
So a file whose hash appears in an event at or before a timestamped head
existed, with that content, by the time of that timestamp, even if no SUMS
file lists it. To check one:

1. Verify the log with the short Python verifier in
   [EVENT_LOG.md](https://github.com/nealmcb/corla-observer/blob/main/docs/EVENT_LOG.md),
   which needs nothing but Python.
2. Confirm that the event with the `seq` named in the SUMS header has the
   hash named there.
3. Find the event recording the file, at or before that `seq`, and compare
   its `file_sha256` with the file's own hash.

This extends the timestamps to everything the tool recorded, without
listing every file in a SUMS file. What it establishes is when the tool had
the file, as the log records it.

## Manifest-hash commitments on Twitter/X

Before this repo's three-layer (git + OpenTimestamps + Sigstore) approach
existed, the practice for several past audits was posting a manifest hash
publicly on Twitter/X in advance of the seed ceremony — the same
commitment principle described above, via a weaker (single, centralized)
channel.

**Broken links in older tweets.** The Secretary of State's site no longer
serves pages at its address without `www.`: a link to `sos.state.co.us/...`
now lands on the home page. That breaks the Audit Center links in the 2021,
2024 and 2025 tweets. The Audit Center is at
https://www.coloradosos.gov/pubs/elections/auditCenter.html, and each
tweet's text is mirrored in the `observerfiles/` folder of its election.

**From the 2026 general on**, the post before the dice roll gives the
SHA-256 of the election's pre-roll `SHA256SUMS` file, but not the file's
name, which doesn't fit in a post. To find the file, compute the hash of
each `SHA256SUMS` file in the election's `observerfiles/` folder and look
for the one that matches; for the 2026 general, from its `2026/general/`
folder:

```
$ sha256sum observerfiles/SHA256SUMS-*.txt
```

- **2026 primary** — [2026-07-13-status-2076696781304574361.txt](../2026/primary/observerfiles/2026-07-13-status-2076696781304574361.txt)
  ([original](https://x.com/nealmcb/status/2076696781304574361)),
  Monday, 2026-07-13, 09:54:30 MDT. SHA-256 of `SHA256SUMS.txt`:
  ```
  cba43b7b811d12a16cb9f673f55d68c0cdab800de693b797d4caacd604df5e2e
  ```
  This checks out: [`SHA256SUMS.txt`](../2026/primary/observerfiles/SHA256SUMS.txt) in
  this repo hashes to exactly this value, its git commit timestamp is
  09:52:41 MDT (two minutes before the tweet), and its OpenTimestamps
  proof is anchored into two Bitcoin blocks (957876 and 957882, mined at
  10:00:32 and 10:48:10 MDT — see the worked example above).

- **2025 coordinated** — [2025-11-17-status-1990454123456803020.txt](../2025/observerfiles/2025-11-17-status-1990454123456803020.txt)
  ([original](https://x.com/nealmcb/status/1990454123456803020)),
  Monday, 2025-11-17, 09:16:58 MST. SHA-256 of `uploadStatus.csv`:
  ```
  c284f31a83d33fe5823629824b7df0f4782e590a72c6a9a8c14bd1d9d8490ca8
  ```

- **2024, primary season** — [2024-07-08-status-1810343570286719070.txt](../2024/primary/observerfiles/2024-07-08-status-1810343570286719070.txt)
  ([original](https://x.com/nealmcb/status/1810343570286719070)),
  Monday, 2024-07-08, 10:01 MDT. SHA-256 of `uploadStatus.csv`:
  ```
  a816078483c789512688cf2ee8fcb12a9185415d56323c9913122bd895bf9cec
  ```

- **2021 coordinated** — [2021-11-15-status-1460273652763545603.txt](../2021/coordinated/observerfiles/2021-11-15-status-1460273652763545603.txt)
  ([original](https://x.com/nealmcb/status/1460273652763545603)),
  Monday, 2021-11-15, 08:49:04 MST. SHA-256 of `sha256sums.txt`:
  ```
  59ad58c2ed8eae0a92479c39cc173db1570000e0fa9f403333a854a3d994b8fe
  ```

- **2018 general** — [2018-11-16-status-1063473017290919936.txt](../2018G/observerfiles/2018-11-16-status-1063473017290919936.txt)
  ([original](https://x.com/nealmcb/status/1063473017290919936)),
  Friday, 2018-11-16, 09:45:00 MST. SHA-256 of `manifest_hash.csv`:
  ```
  c3f23655ae1bcb721255288f8e44d9a3ebdedb885c4bcb4cfc2b8986d1aaf5ee
  ```

These posts committed to manifest data, not to cast vote records. No
public commitment was made before the dice roll to the cast vote records
of audits before 2026, so for those audits the manifests can be shown not
to have been altered afterwards, but the CVRs compared with the hand
counts generally can't.

## Further reading / where this could go next

- [IETF SCITT](https://datatracker.ietf.org/wg/scitt/about/) (Supply Chain
  Integrity, Transparency, and Trust) is standardizing exactly this pattern —
  signed statements registered in a public transparency log — with a
  standard signing/receipt format, rather than the more ad hoc combination
  used here.
- [SLSA](https://slsa.dev/) (Supply-chain Levels for Software Artifacts),
  also originating at Google, standardizes machine-readable *provenance*
  statements ("this artifact was produced by X, from source Y, at time Z"),
  which maps naturally onto "this evidence set was collected from the
  Secretary of State's site at this time."
- **Other timestamping services under consideration.** We're looking for
  services that are quicker to confirm and easier for newcomers to check.
  Services come and go, so each is judged both on its own front end and on
  the record it relies on:
  - [Keybase](https://keybase.io/): signed statements tied to a user's
    public identity; Keybase's own Merkle tree root is anchored to the
    Stellar blockchain.
  - The [Internet Archive](https://web.archive.org/)'s Save Page Now: a
    capture of a public URL, dated by the Archive.
  - [Software Heritage](https://www.softwareheritage.org/)'s "Save Code
    Now": an archived copy of this repository, dated by the archive's visit,
    with a permanent identifier for each file and commit.
  - [Zenodo](https://zenodo.org/): a citable, dated copy of a release of
    this repository, with a DOI.
