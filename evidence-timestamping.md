# Timestamping audit evidence: why, and how we do it

This document explains, for people new to risk-limiting audits (RLAs) and to
cryptographic timestamping alike, why audit evidence — starting with the
ballot manifests in directories like
[`2026/primary/files/`](2026/primary/files/), and eventually extending to
redacted cast vote records (CVRs) as those get added — gets a public,
independently-verifiable timestamp, and exactly how that's done in this repo.
See the [README](README.md) for background on the data itself, and
[The Colorado Risk-Limiting Audit Project (CORLA) and related work](http://bcn.boulder.co.us/~neal/elections/corla/)
for background on Colorado's RLA process generally.

## Why this matters: the "dice roll" and commitment

A risk-limiting audit starts with a public **random seed generation ceremony**
— the "dice roll" — where members of the public roll ordinary dice to produce
a random seed. That seed drives the pseudo-random number generator that
selects which ballots get pulled for hand audit.

The whole point of rolling real dice in public is that nobody, including
election officials, can predict or influence which ballots will be selected.
But that guarantee only holds if the **ballot manifests** (the county-by-county
inventories of how many ballots exist in each batch, which the sampling
algorithm draws against) are locked in *before* the seed exists. If a manifest
could still be edited after the seed is public, someone could in principle
work backwards from the seed to figure out which specific ballots would be
picked, and adjust the manifest (or worse) accordingly. Even without any bad
intent, if there's no public proof of *when* the manifest was fixed, a
skeptical observer has no way to rule that scenario out.

So we need a way to publicly and irrevocably prove: *"this exact set of
bytes existed, unchanged, at this exact time — before the dice were rolled."*
That's a **cryptographic commitment**, and the goal is to make it verifiable
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

## Our approach: three independent, free, public layers

Rather than pick one mechanism and hope it holds up, we commit the same
digest through three independent public systems. An observer only needs to
trust *at least one* of these to be convinced the evidence wasn't altered
after the fact — and all three are free, standards-based, and independently
verifiable without any account or special access.

### 1. Git commit + public GitHub push

We compute SHA-256 hashes of every evidence file into a single
`SHA256SUMS.txt`, and commit that alongside the files themselves to this
repo, which is pushed to the public mirror at
[github.com/nealmcb/auditcenter](https://github.com/nealmcb/auditcenter).
This is the weakest of the three layers on its own (GitHub could in theory
alter timestamps, and a git commit date is self-reported by the client), but
it's simple, gives anyone a durable public copy, and the commit hash is
itself a cryptographic digest of the tree contents — useful as a stable
reference for the other two layers.

### 2. OpenTimestamps (Bitcoin-anchored)

[OpenTimestamps](https://opentimestamps.org/) is a free, open protocol built
on top of the Bitcoin blockchain. Instead of trusting one server, it submits
your file's hash to several independent "calendar" servers, which each
aggregate many people's hashes into a single Merkle tree and periodically
commit the tree root into a real Bitcoin transaction. The result is a small
`.ots` proof file that lets *anyone*, using free open-source software and a
copy of the Bitcoin blockchain (or a public block explorer), verify that your
exact file hash existed at or before a specific Bitcoin block — without
needing to trust OpenTimestamps, us, or any single calendar server.

We generate this with the [`ots`](https://github.com/opentimestamps/opentimestamps-client)
command-line client:

```
$ ots stamp SHA256SUMS.txt
```

This produces `SHA256SUMS.txt.ots`. Right after stamping, the proof is
"pending" — the calendar servers have your hash queued for their next Bitcoin
transaction, which usually appears within minutes and gets fully confirmed
within an hour or so. You can check status any time with:

```
$ ots verify SHA256SUMS.txt.ots
```

Once confirmed, this is the strongest layer: it depends on nothing but the
Bitcoin network continuing to exist, which is about as close to "nobody can
quietly go back and change this" as currently practical.

### 3. Sigstore / Rekor (public transparency log)

[Sigstore](https://www.sigstore.dev/)'s **Rekor** is a free, public
[transparency log](https://github.com/transparency-dev) — the same idea
pioneered by Google's Certificate Transparency project (RFC 6962) for TLS
certificates, generalized (via Google's Trillian log server) into a
log anyone can write signed statements into. Every entry is added to an
append-only Merkle tree whose root is regularly published, so nobody —
including the people running Rekor — can quietly remove or alter an entry
without it being detectable.

We sign the same `SHA256SUMS.txt` and submit it with
[`cosign`](https://github.com/sigstore/cosign):

```
$ cosign sign-blob --bundle SHA256SUMS.txt.cosign-bundle SHA256SUMS.txt
```

This returns a Rekor **log index** (a public entry number) within seconds —
much faster than waiting for Bitcoin confirmation. Anyone can independently
look up that exact entry:

```
$ rekor-cli get --log-index <the index number>
```

and confirm it contains the same SHA-256 hash, with no dependency on us
still having the file, our GitHub account, or our signing key.

*Note on the current prototype:* the signing key used for the 2026 primary
dice-roll run was a freshly-generated, throwaway keypair, not tied to any
verified identity — fine for proving "a consistent signer logged this
entry," but not yet proof of *who*. A better long-term setup is Sigstore's
"keyless" signing, which binds the signature to a real, OIDC-verified email
identity (e.g. via a Google/GitHub login) instead of a bare key file, so
the public Rekor entry itself says who signed it.

## Worked example: 2026 primary dice roll (manifests)

For the 2026 primary dice roll, the concrete artifacts are in
[`2026/primary/`](2026/primary/). CVRs aren't part of this worked example yet
— once redacted CVRs are added to the repo, they'll go through the same
three-layer process described above.

- [`files/`](2026/primary/files/) — county manifest CSVs collected from
  Colorado's Audit Center (San Juan County hand-counts and is excluded from
  the audit entirely)
- [`observerfiles/`](2026/primary/observerfiles/) — manifests and redacted
  CVRs obtained directly from counties, plus notes on anything found
- `SHA256SUMS*.txt` (+ matching `.ots` / `.cosign-bundle`) — SHA-256 digests
  of the evidence files above, timestamped as described below

We never overwrite a `SHA256SUMS*.txt` once it's been stamped and pushed —
each update to the evidence set gets a new version (`SHA256SUMS.txt`,
`SHA256SUMS.v2.txt`, ...) with its own OTS and Rekor proof, so every
commitment we ever made stays independently checkable, even after later
files supersede it.

To verify any version yourself (substitute the version you're checking):

```
$ sha256sum -c SHA256SUMS.v2.txt          # confirm the files match the recorded hashes
$ ots verify SHA256SUMS.v2.txt.ots        # confirm the Bitcoin-anchored timestamp
$ cosign verify-blob --bundle SHA256SUMS.v2.txt.cosign-bundle SHA256SUMS.v2.txt
                                           # confirm the Rekor transparency-log signature
```

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
