# Timestamping audit evidence: why, and how we do it

This document explains, for people new to risk-limiting audits (RLAs) and to
cryptographic timestamping alike, why audit evidence gets a public,
independently-verifiable timestamp, how you can check that yourself on Mac,
Windows, or Linux, and how it's produced in this repo. That evidence starts
with the ballot manifests in directories like
[`2026/primary/files/`](2026/primary/files/), and extends to redacted cast
vote records (CVRs), which are being piloted in select counties for the
2026 primary.
See the [README](README.md) for background on the data itself, and
[The Colorado Risk-Limiting Audit Project (CORLA) and related work](http://bcn.boulder.co.us/~neal/elections/corla/)
for background on Colorado's RLA process generally.

**Just want to check the evidence yourself?** Skip straight to
["How to verify this yourself, on Mac, Windows, or Linux"](#how-to-verify-this-yourself-on-mac-windows-or-linux)
below. The background and how-we-built-it details follow after that.

*This explanation and tips on verification are hot-off-the-presses — this
whole approach is a first shot, and still a bit clunky (three different
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

## How to verify this yourself, on Mac, Windows, or Linux

We commit the same digest through three independent public systems, so you
only need to trust *at least one* of them — pick whichever is easiest for
you. Here's a concrete example: confirming that
[`observerfiles/Weld_CVR_Export_20260709140755.csv`](2026/primary/observerfiles/Weld_CVR_Export_20260709140755.csv)
is the exact file we timestamped, not something swapped in afterward.

**First, find the file's recorded hash.** Every `SHA256SUMS*.txt` file lists
one line per evidence file. Open [`2026/primary/SHA256SUMS.v4.txt`](2026/primary/SHA256SUMS.v4.txt)
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
  and drag in both [`SHA256SUMS.v4.txt`](2026/primary/SHA256SUMS.v4.txt) and
  [`SHA256SUMS.v4.txt.ots`](2026/primary/SHA256SUMS.v4.txt.ots) — it verifies
  the Bitcoin anchor in your browser.
- **Or, if you're comfortable with a terminal:** `pip install opentimestamps-client`
  (Python and pip both have native Mac and Windows installers), then:
  ```
  $ ots verify SHA256SUMS.v4.txt.ots
  ```

### 3. Check the Sigstore/Rekor transparency-log entry

This proves someone published that same hash to a public, tamper-evident log
at a specific time, independent of Bitcoin or GitHub.

- **No install, any platform**: go to [search.sigstore.dev](https://search.sigstore.dev/)
  and paste in the hash from `SHA256SUMS.v4.txt` — it shows you the public
  log entry directly in your browser.
- **Or, if you're comfortable with a terminal:**
  - Mac: `brew install cosign`
  - Windows: `choco install cosign`, or download the `.exe` from the
    [cosign releases page](https://github.com/sigstore/cosign/releases)
  - Linux: see your package manager, or the same releases page
  - Then, on any platform:
    ```
    $ cosign verify-blob --bundle SHA256SUMS.v4.txt.cosign-bundle SHA256SUMS.v4.txt
    ```

If any one of these three checks passes, you've independently confirmed the
evidence wasn't altered after it was timestamped — without needing to trust
us, GitHub, or any single calendar/log operator.

## Why three separate layers

Each layer has a different weak point, so relying on all three together
means an observer isn't stuck trusting any single one:

- **Git commit + public GitHub push**: simple and gives anyone a durable
  public copy, but GitHub could in theory alter timestamps, and a commit
  date is self-reported by the client. Weakest layer alone, but the commit
  hash is a useful stable reference for the other two.
- **OpenTimestamps**: anchored to the Bitcoin blockchain, so once confirmed
  it depends on nothing but Bitcoin continuing to exist — about as close to
  "nobody can quietly go back and change this" as currently practical. The
  tradeoff is confirmation can take from minutes to an hour or more.
- **Sigstore/Rekor**: a public, append-only transparency log (the same idea
  as Google's Certificate Transparency project, generalized via Google's
  Trillian log server) — entries can't be quietly removed or altered without
  it being detectable. Confirms within seconds, much faster than Bitcoin, but
  is a newer, less battle-tested system than Bitcoin itself.

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

*Note on the current prototype:* the signing key used for the 2026 primary
dice-roll run was a freshly-generated, throwaway keypair, not tied to any
verified identity — fine for proving "a consistent signer logged this
entry," but not yet proof of *who*. A better long-term setup is Sigstore's
"keyless" signing, which binds the signature to a real, OIDC-verified email
identity (e.g. via a Google/GitHub login) instead of a bare key file, so
the public Rekor entry itself says who signed it.

## Worked example: 2026 primary dice roll

For the 2026 primary dice roll, the concrete artifacts are in
[`2026/primary/`](2026/primary/):

- [`files/`](2026/primary/files/) — county manifest CSVs collected from
  Colorado's Audit Center (San Juan County hand-counts and is excluded from
  the audit entirely)
- [`observerfiles/`](2026/primary/observerfiles/) — manifests and redacted
  CVRs obtained directly from counties, plus
  [`2026-primary-details.md`](2026/primary/observerfiles/2026-primary-details.md),
  notes on what was found and confirmed for this election
- `SHA256SUMS*.txt` (+ matching `.ots` / `.cosign-bundle`) — SHA-256 digests
  of the evidence files above, timestamped as described above

We never overwrite a `SHA256SUMS*.txt` once it's been stamped and pushed —
each update to the evidence set gets a new version (`SHA256SUMS.txt`,
`SHA256SUMS.v2.txt`, ...) with its own OTS and Rekor proof, so every
commitment we ever made stays independently checkable, even after later
files supersede it.

This first pilot run had some last-minute churn — a few counties' manifests
weren't posted yet at roll time, one publishing bug briefly served the wrong
county's data, and evidence trickled in from observers throughout the
morning — hence four versions instead of one. `SHA256SUMS.v4.txt` is the
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
- Moving from a throwaway signing key to Sigstore's keyless/OIDC signing
  would let the public Rekor entry itself identify who vouched for the
  evidence set, rather than just an anonymous keypair.
