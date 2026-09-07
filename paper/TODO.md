Ask ChatGPT / Codex to act as a CS election auditing expert / reviewer and review the paper and the database and the auditcenter repo and confirm samples an/or all claims in the paper, citing any references that should have been included etc.

Ensure that overall framing / message is enormous trove of evidence across contests in Colorado.
Now cleaned and available.

Note that we haven't located all the data.
Deal with data gaps: 2017 auditcenter, discrepancy reports we don't have,
Consider how to frame and present missing data that we haven't even asked for yet.

Note room for improvement in the audits

Vet the conclusion language relating to Random sampling approach is not always independent across counties, sometimes constrains statistical techniques that can be used.

Avoid casting aspersions on the SoS or the audits or the elections

Get input from John, Edouard, ??

WTF? 6.4 Data-quality gaps in the discrepancy record itself. Can't leave that gap with so much unexplained!

consider moving section 6 to proceed section 5 given the back-reference now.

Rename section 4 to "Contest categories". Emphasize contest type stats, not coverage, in section 4.
Droped secion 4.4.

Perhaps drop most of section 4.3 or fix the rude treatment of "no comparison record" based on published theory.

either manually fix the classification of ”City of Fort Collins Mayor” (2025) and perhaps the others
and remove the paragraph that explains the gap we fixed.

Still useful actually: Directly targeted contests are consistently a small minority of the total — never more than about 10%, and often closer to 4% in the larger general elec- tions, where the number of small down-ballot con- tests grows faster than the number of contests for- mally selected to drive sampling.

In the intro, explain the "blind" ballot entry: audit boards don't know what to expect on the ballot,
though they do check that it is the right style. This also means they get few hints that they
may have not found the right ballot at all.  Intentional design to avoid any temptation to
make the answers come out right [theres' a better colloquial expression for that that I can't remember.]

Consider either including this follow-on work, or at least noting that the existing audits are not fully publicly verifiable and why.

  Several Colorado counties have independently begun piloting mechanisms to publish cast-vote-record data (redacted when necessary due to rare ballot styles) before the random seed is drawn. That is a stronger, forward-looking form of provenance than the source-file traceability this reconstruction establishes (§3.5): it would let an outside observer confirm which records existed prior to the draw itself, rather than only trace a reconstructed record back to the export file it came from — extending public verifiability beyond what our own after-the-fact approach can offer, and worth documenting in its own right as those pilots mature.

define the term "voting system" to include the scanning, vendor interpretation, adjudication process updates, thru the upload to CORLA.

Review and decide whether the normalized format Claude has created is indeed correct, worthwhile, helpful, clear, adequate, future-proof.

Check out Neal's early provisional text to consider for describing target contest guidelines.
Look for actual SoS goals instead
 whose margin of victory would lead to an initial sample size that is large enough to provide useful opportunistic auditing, but also not so big that....


Note missing manifests for 2023-coordinated
 (57): already explained elsewhere in this repo, and reconfirmed here rather than re-derived – docs/DATA_DICTIONARY.md’s “Filename/directory-layout conventions by year” table documents that Douglas, Phillips, Delta, Moffat, Summit, and Sedgwick’s manifests were never archived by the Wayback Machine (this project’s own live scrape never captured them either), so those 6 fall back to batchCountComparison.csv instead of a real manifest file. 6 missing
San Juan = 7 of 64 absent, 57 present – matches.

Figure out what happened for Boulder in 2020-primary
2020-stateprimary (62 at the top level): Boulder County is not genuinely missing – it ran a separate, self-contained RLA instance that election, filed in its own 2020/statePrimary/boulder/ subtree (manifest_boulder.csv, plus its own round_1/round_2 comparison files), which this survey’s registry deliberately excludes from the top-level scan (consistent with election_layouts.py’s own documented handling). Combined, 2020-stateprimary covers all 63 non-San-Juan counties.

Figure out 2021-coordinated Mineral county
 2021-coordinated (62): genuinely missing Mineral County, beyond San Juan – no manifest file, and no Mineral filename anywhere in the 2021 tree at all (confirmed absent from contests_by_county.csv too).


Review the "filetype signature" work and the way that section about how changes over time is handled

Separately: confirmed the zero_discrepancy_count rename (replacing
other_count) is a permanent software-version change, not something that
happens specifically "when there's an IRV audit." 2026-primary already
uses zero_discrepancy_count with zero IRV export directory that cycle.
The same CORLA codebase upgrade that added zero_discrepancy_count also
added general RAIRE/IRV assertion support, so the two landed together,
but they're separate facts -- the field rename applies every year from
2025-coordinated on regardless of IRV; the extra IRV-specific files
(assertions-csv, ranked_ballot_interpretation.csv, summarize_IRV.csv,
tabulate_plurality.csv) only appear when a jurisdiction actually runs an
IRV audit, so far just 2025's Larimer pilot.

Sections this could touch, depending what we decide to do:
- §2 background: the CORLA-software-version/schema-evolution point above,
  if we want to name the zero_discrepancy_count/IRV-support coincidence
  at all.
- §3.1: the "single 2025 instance uses...IRV..." sentence -- already
  fairly accurate, but could note the export is Larimer-only, not
  statewide.
- §3.5: "scoped out of the risk-bearing tables" wording -- should say
  "not onboarded at all," not scoped out of one specific table category.
- §4: Fort Collins Mayor paragraph already added; Town of Estes Park is a
  second, not-yet-named instance of the same kind of gap.
- §6 discrepancies: if we ever do import 2025-irv, IRV/RAIRE assertion
  "discrepancies" aren't the same kind of thing as Kaplan-Markov
  o1/o2/u1/u2 counts -- Neal's own instinct is to leave them out of the
  discrepancy-count reporting entirely rather than force a mapping.

Not deciding any of this now -- revisit after the rest of the text
review is done.



Round-by-round reporting is a bigger, separate topic than §3 currently lets
on. Checked against the private analysis repo directly: this is NOT
incomplete human export work, it's a confirmed CORLA software behavior.
ComparisonAudit.addContestCVRIds() always appends, so contest_cvr_ids
accumulates across rounds rather than resetting -- every round's export of
that field reflects the FINAL accumulated state, not that round's own
selection. A second, compounding bug: the comparison-file SQL joins on
audit_reason rather than contest identity, so any ballot drawn for any
same-type targeted contest gets logged against every contest on that
ballot. Documented in SELECTION_FLAWS.md (worked example: Pueblo County
Commissioner - District 2, 2024 general, all three rounds byte-identical)
and SELECTION_FLAWS_SURVEY.md (22 of 22 audited rounds, 2019-2025, show at
least one symptom). No draft SoS/CDOS feedback document found under that
description. Open decision: ignore round-level granularity entirely and
describe only final-round/cumulative state throughout (closest to current
practice), allude to it briefly as a known limitation, or give it its own
subsection -- ask me to draft any of these when you're ready.

In the intro or background, frame the paper as reconstructing the 10
years of audit data based on scrapes of the auditcenter's manually
constructed export data -- which had gaps -- not necessarily the data
used internally by CORLA itself. (Montrose/Montezuma in §3.4 is a
concrete example of exactly this distinction: the export we scraped was
wrong, but the audit's own internal data was not.)



Old-Clarity-ENR cross-check status (question from Neal 2026-09-06): what
dataset-integrity verification exists using old Clarity election-night-
reporting pages to check contest names/margins independently? Answer as
of this writing: `auditcenter_analyze-private/src/auditcenter_analyze/
enr_crosscheck.py` exists for exactly this -- parses the SOS's own
unofficial Clarity ENR workbook (one sheet per contest, county rows, a
trailing Total row) into the same `ConsolidatedContest` shape used for
CORLA's own totals, with a per-county-resolved `find_discrepancies` for
tracking down *why* a statewide total differs, not just that it does. It
generalizes an earlier ad hoc, Governor-REP-only, Weld-only check
(`anonymize-weld-CVR`'s `ENR_vs_CVR_crosscheck.md`) into a statewide,
all-contest routine, per that repo's own TODO Phase 4. Status: the module
and its tests (`tests/test_enr_crosscheck.py`) exist; no evidence found of
it having actually been RUN as a full statewide sweep across multiple
elections yet (no output/report file on disk) -- worth running for real
and considering whether a resulting cross-check belongs in §5 alongside
the existing PRNG-selection-reproduction and typed-discrepancy validation
channels, as a third independent check (this time against contest
names/vote totals rather than ballot selection or discrepancy counts).



===
2025-irv: investigated directly against the raw exports. It's Larimer
County only -- the Fort Collins/Loveland municipal races from the same
November 2025 coordinated election, exported a second time in a separate
2025-irv/ directory because Fort Collins uses IRV for some races. Most of
its contests are identical duplicates of what's already in 2025-coordinated
(Loveland's races, the ballot issues, Councilmember District 5). But three
went through the separate RAIRE/IRV-assertion framework -- Fort Collins
Mayor (formally targeted, real audit) and Councilmember Districts 1 and 3
(evaluated for IRV assertions but never formally targeted). Of those,
Fort Collins Mayor is a real, confirmed problem: the main 2025-coordinated
export shows it as audit_reason=opportunistic_benefits,
audited_sample_count=0 (looks like it got no direct RLA attention), while
2025-irv's own record shows audit_reason=county_wide_contest,
random_audit_status=risk_limit_achieved, audited_sample_count=240 -- a
real, formally targeted, completed audit, just recorded only in the
export this paper's §4 coverage analysis doesn't read. So §4's coverage
classification currently miscounts this one contest as
opportunistic-only. Also: §3.5's "one further instance's
IRV audit is scoped out of the risk-bearing tables for
the same reason" is imprecise -- 2025-irv has the full modern contest_csv
file family (contest.csv, contest_comparison.csv, contest_selection.csv),
unlike the pre-2019 ballot_list-era elections it's currently grouped
with; it's excluded because its risk methodology (RAIRE/IRV assertions)
differs from Kaplan-Markov, not because the data is structurally
impoverished. Not fixed here -- your call whether to correct Fort
Collins Mayor's coverage classification using the 2025-irv record, or
just flag it explicitly as a known exception.

Full 2025-irv assessment (2026-09-06), for the "what to do about it"
decision after the rest of the text review is done. Reusable script:
auditcenter_analyze-private/scripts/compare_2025_irv_vs_coordinated.py.

All 41 contests in 2025-irv/contest.csv also appear in 2025-coordinated's
own contest.csv. Ten conflict on audit_reason/random_audit_status/
audited_sample_count, in both directions -- not just Fort Collins Mayor
(undercounted in the main export) but also Larimer County Ballot Issue 1A
(the opposite: undercounted in 2025-irv, which shows it as opportunistic/0
when the main export shows a real, completed, 205-sample audit). Prop LL,
Prop MM, and four multi-county school-district seats (St. Vrain, Thompson)
show differing min_margin between the two exports -- likely because
2025-irv's figures for genuinely multi-county contests reflect only
Larimer's own local slice, not the full contest -- unverified hypothesis,
not confirmed.

Two more real coverage gaps beyond Fort Collins Mayor: Town of Estes
Park's two ballot questions have zero comparison rows in the main export
(so §4 likely misclassifies them as "no comparison record") but 7 real
rows each in 2025-irv. St. Vrain Valley's four director races are the
reverse (real rows in the main export, zero in 2025-irv) -- harmless,
since the main export already has the real data there. Three tiny
Larimer public-improvement-district issues have zero comparison rows in
BOTH exports -- "no comparison record" is correct for those three, not a
gap.

2025-irv itself is not onboarded into the crossdb at all -- no
election_layouts.py entry, zero rows anywhere keyed to it. It's not that
it's excluded from just the "risk-bearing tables" (§3.5's current
wording implies partial inclusion); nothing about it is imported. What
IS imported is only 2025-coordinated's own (partially wrong, per above)
version of these same Larimer contests.
===


CORLA software versioning, investigated 2026-09-06 (checked directly via
gh api/search, not guessed). No version number appears anywhere in any
export file checked (CSV headers, XLSX docProps metadata, HTML report
pages). The repo landscape is more tangled than REFERENCES.md's current
two-repo citation implies:
- FreeAndFair/ColoradoRLA (archived 2018) and democracyworks/ColoradoRLA
  (archived 2019) both have real semver release tags.
- Three repos, not two, and the fork direction runs the opposite way from
  a first guess. cdosco/colorado-rla (created 2018) looks canonical by
  name and history, but its own LAST COMMIT EVER (2025-09-16) is literally
  "Merge pull request #1 from cdos-rla/master" -- it pulls FROM cdos-rla,
  not the other way around. cdos-rla/colorado-rla is a fork of cdosco
  (confirmed via the GitHub API) but is the one with actual ongoing
  development -- most recent commit 2026-07-08, and its recent history is
  dominated by merged PRs from DemocracyDevelopers/main (dependabot
  bumps, an "Add example assertions from NSW data" PR, doc fixes,
  links to DemocracyDevelopers' own educational materials). A third repo,
  DemocracyDevelopers/colorado-rla, forks cdos-rla (not cdosco) and was
  pushed as recently as 2025-12-19 -- almost certainly where
  DemocracyDevelopers' own day-to-day IRV/RAIRE work happens before PRs
  go up. cdosco and cdos-rla have DIVERGED (confirmed via GitHub's compare
  API): cdos-rla has one commit cdosco lacks (the 2026-07-08 one, the most
  recent real change to either), cdosco has one commit cdos-rla lacks
  (the Sept 2025 merge-PR commit itself).
- Versioning: cdosco/colorado-rla has ZERO tags, ever. cdos-rla/colorado-rla
  has exactly two tags (2.4.23, 2.3.70.1), both dated the same day
  (2023-11-18) -- looks like a one-time snapshot, not ongoing release
  discipline.
- DemocracyDevelopers/raire-service (active, pushed 2026-08-28) is a
  CORLA-to-RAIRE bridge microservice (CORLA calls into it, not the
  reverse); two more DemocracyDevelopers repos
  (Colorado-irv-rla-educational-materials, Utilities-and-experiments) are
  also live -- all Vanessa Teague's group's own work for the RAIRE/IRV
  side of this.
- JohnLCaron/rla-kotlin ("partial port of classes from colorado-rla",
  pushed 2024-10-19) is almost certainly John Caron's own work.
- The au.org.democracydevelopers.corla package (IRV/RAIRE assertions,
  including the Assertion class zero_discrepancy_count comes from) first
  lands around 2024-05-30, confirmed via that file's own commit history.

Real problem for citing any of this precisely: neither cdosco nor cdos-rla
has ever tagged a release, so there's no clean version number for "which
software produced this year's export" -- only commit SHAs/dates, and
even those require knowing which of the three repos actually ran in
production for a given election. We'll want to reference this repo
landscape somewhere -- FAQ, appendix, or the normalized-database
documentation -- once it's sorted out.


Draft questions for Vanessa (ask her before bothering Eddie, since her
team did the actual IRV integration and would know the deployment
history directly):
- Which repo/branch actually ran in production for the 2025-coordinated
  audit and the 2025-irv Larimer pilot -- cdos-rla/colorado-rla directly
  (it looks like the actively-developed one), the DemocracyDevelopers
  fork, or something else not yet found?
- Is there any internal versioning/changelog/deployment-tag convention
  DemocracyDevelopers or CDOS uses that isn't visible as GitHub tags?
- Given zero_discrepancy_count is now used statewide (not just for IRV
  contests) starting 2025-coordinated, was that field rename intentional
  and documented anywhere, or an incidental side effect of the
  Assertion-class refactor that added IRV support?
- Any plans to formally tag releases going forward, given neither
  cdosco nor cdos-rla currently has any?

corlasoftware citation checked, not changed: the state's own auditCenter
page has linked to github.com/cdos-rla/colorado-rla consistently since at
least 2022 through the most recent 2025-11-04 snapshot -- confirmed
directly by grepping the mirrored HTML. REFERENCES.md already cites that
same URL, correctly, per the "whatever the auditcenter itself points to
is official" rule. This is a better citation than it first looked: given
cdos-rla is the actively-developed repo (see above), not a neglected
fork, the state is pointing the public at the right one.

For the eventual, more detailed feedback/proposal to Eddie/CDOS (not the
short missing-data email already sent): add a note recommending they
adopt real software versioning. As it stands, neither cdosco/colorado-rla
nor cdos-rla/colorado-rla (the one the state officially links to) has
ever tagged a release -- cdos-rla has exactly two tags, both dated the
same day in 2023. There's no way for an outside party to know which
software version produced a given year's export, which matters directly
for reproducibility claims like this paper's own §5.


Boulder County's 2023 RCV/IRV mayoral audit, investigated 2026-09-07
(checked directly, not guessed): a genuinely separate system, not CORLA.
CORLA had no IRV capability until the 2024-05-30 codebase change already
documented above, so Boulder built its own toolchain
(github.com/BoulderCounty/rcv-rla) on SHANGRLA (Stark/Blom/Conway/
Stuckey/Teague) and RAIRE (Blom's IRV assertion generator), plus a
Manual Vote Review tool adapted from Dan King/Laurent Sandrolini's 2019
San Francisco DA IRV audit. Rule4 (rule4.com), a Boulder-based
cybersecurity/infrastructure firm, operationalized and maintains that
repo -- the same Rule4 already on the list to get an early look at the
chain-of-custody note, which makes them a natural contact for this too.

Checked the main 2023-coordinated CORLA export directly for the contest
(real name: "City of Boulder Mayoral Candidates" -- not "City of Boulder
Mayor", which is why it didn't turn up on the first pass): zero rows in
every operational file (contest.csv both rounds, both comparison-file
names, contestSelection.csv, contestsByCounty.csv, tabulate.csv). The
name appears exactly once in the whole tree, in canonicalListFinal.csv
(the general statewide contest/candidate reference list, not an audit
record). This is a cleaner separation than 2025-irv's Fort Collins Mayor
case (§4's known exception) -- that one showed up in the main export,
just miscategorized as zero-sample opportunistic; this one doesn't show
up in CORLA's audit-relevant files at all, consistent with CORLA having
no IRV capability whatsoever in 2023.

We have no data from the actual 2023 audit run itself, i.e. from
Boulder's own separate SHANGRLA/RAIRE process: the public repo is
marked draft, and its own data directories (MVR/data/contest_sample/*)
contain only synthetic placeholder content (a "TEAM MASCOT" contest with
candidates "ANGEL"/"BEAR"/"CARDINAL"), not Boulder's real November 2023
numbers. Worth asking Boulder County directly, or Rule4, whether the
real run's samples and discrepancies were preserved anywhere -- and if
so, note that a SHANGRLA/RAIRE assertion-based audit's discrepancies
aren't natively expressed as Kaplan-Markov o1/o2/u1/u2 overstatement/
understatement counts the way §6 categorizes CORLA's own comparison-audit
discrepancies, so translating between the two systems (if attempted at
all) would need its own explicit mapping, not a direct reuse of §6's
categories.

Separately notable: the current Colorado rules (effective 8/20/2026)
now have a Rule 26.10 explicitly on "Auditing a ranked voting contest" --
26.10.1 makes standard IRV contests eligible for the state-administered
RLA itself (matching what 2025-irv piloted); 26.10.2 requires a separate
independent audit for any OTHER ranked-voting method. Boulder's 2023
improvised toolchain is exactly the kind of gap this rule appears to
have been written to formalize.



Discrepancy-typing follow-up (2026-09-06, per Neal): §6 now reports a real
o1/o2/u1/u2 breakdown by election (Table 4) plus a small validation table
in §5.3 (Table 3, 477 targeted contests, independently-derived vs CORLA's
own reported counts, exact match). Not attempted: differentiating
discrepancy rate by whether a county's ballots carry a machine-imprinted
ID the audit board can read directly, vs. tabulator/batch/position
bookkeeping only -- flagged explicitly as future work in new §6.5. No such
variable is currently captured anywhere in this reconstruction; building
it needs county-by-county research (which vendor/config each county runs)
outside this submission's scope. Other untried candidate covariates:
ballot volume, voting-system vendor (Dominion vs. Clear Ballot).


Provenance background and evidence for the paper (after submission
review, per Neal 2026-09-06): add the existing tweets cataloging
manifest-hash commitments (already mirrored as files in this project, per
the 2026-07-24 commit "Catalog historical manifest-hash commitment
tweets"), and a link to the auditcenter hashing/provenance page. §7
already gestures at "several Colorado counties have independently begun
piloting mechanisms to publish cast-vote-record data, with cryptographic
provenance guarantees" without citing specifics -- this would ground that
sentence with real evidence instead of a generic description. Deliberately
held for AFTER the Sept 7 submission goes in, per Neal's own framing.


## Before final submission: anonymization pass (added on the evtwote2026-submission branch)

This branch's dev-only HTML comments (at the top of each sections/*.md
file) and REFERENCES.md's own editorial notes still contain "Neal"
references (e.g. "per Neal's explicit instruction", "self-citation
(Rivest, not Neal)"). These are stripped automatically from the compiled
PDF (see latex/md2latex.py's strip_dev_markup) and are NOT present in
that PDF, but they ARE present in this branch's own paper.md (a plain
concatenation of sections/*.md, dev comments included) and in
REFERENCES.md itself. Per plan: squash this branch's history and scrub
these specific mentions in one final anonymization pass right before
depositing/linking this repo for review -- not needed on every
intermediate commit before then.

## Before final submission/deposit: anonymization pass on this file itself

This TODO file names real third parties (e.g. "John, Edouard", "John
Caron") in several planning notes above. Fine for an internal working
file, but scrub before this repo is actually deposited/linked for
review -- same final pass noted in the repository root's own TODO.md.

## Repo-structure refinement (2026-09-07, Neal): separate the paper repo from auditcenter

After more thought, the plan for this whole reproduction package is
changing:

- **Move the actual paper-support package (this `paper/` directory,
  `corla_results/`, `reproduce_paper.ipynb`, `cross_election.db`, and
  `DATABASE.md`) into a new, separate, initially-private repository**
  (working name: `corla10`) -- not nested inside `auditcenter` as a
  branch, its own repo.
- That new repo's own reproduction instructions should reference
  `auditcenter` (the raw CORLA export mirror) as a **separate**
  repository/dependency -- clone it alongside, don't re-bundle a copy of
  its raw data inside the new repo.
- Once `corla10` exists and the reproduction actually works end to end
  from it, **wipe this `evtwote2026-submission` branch back to clean**
  on `auditcenter` -- remove the accumulated `REVIEW.md` files and
  review-cycle commits entirely, so `auditcenter` goes back to being
  just the raw data mirror it always was, with nothing paper-specific on
  any of its branches.
- Then give GitHub Copilot a genuinely fresh start: a clean new task
  against `corla10` (once it's ready), rather than another pass on this
  branch's accumulated history.
- Also still want a truly **anonymous** hosting setup for `corla10` (not
  just an anonymized-proxy view of a repo under Neal's own account --
  see the earlier anonymous.4open.science discussion) before this is
  actually used for real review.

Not started yet -- this is the plan, recorded here before acting on it.
