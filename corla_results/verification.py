"""Reproduces the paper's §5 (dataset integrity verification): the
selection-reproduction PRNG check (Table 2) and the typed-discrepancy
validation against CORLA's own reported counts (Table 3).

Scope note: this module implements CORLA's actual selection algorithm
(`sha256_random_numbers`, below -- confirmed by direct reading of its
published source code, §5.1). Running that algorithm across every
checkable contest to reproduce Table 2's full 732/748 sweep requires
reconstructing each contest's exact ballot "domain" (the ordered
concatenation of one or more counties' manifests the PRNG counter
indexes into) using the same population figure CORLA's own software
used -- `manifest_batches` stores each county's own local batch
positions, but the exact per-contest domain size (e.g. whether a
party-primary contest's domain is the full county manifest or a
narrower card-style-filtered population) is not yet re-derived from
this database in this package, so a worked end-to-end demo is not
included here -- only the algorithm itself, plus `TABLE_2` and `TABLE_3`
reporting the full sweep's already-verified results as reference values.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass


def sha256_random_numbers(seed: str, count: int, domain_size: int) -> list[int]:
    """Generate `count` picks in [1, domain_size] via CORLA's own PRNG.

    Matches `us.freeandfair.corla.crypto.PseudoRandomNumberGenerator`: for
    each 1-based index i, hash "{seed},{i}" with SHA-256, interpret the
    digest as a big-endian integer, and take (int mod domain_size) + 1.
    Picks are not deduplicated -- SHANGRLA-style comparison-audit sampling
    is with replacement, so the same ballot can legitimately be drawn more
    than once.
    """
    if domain_size <= 0:
        raise ValueError(f"domain_size must be positive, got {domain_size}")
    picks = []
    for i in range(1, count + 1):
        digest = hashlib.sha256(f"{seed},{i}".encode("utf-8")).digest()
        value = int.from_bytes(digest, byteorder="big")
        picks.append(value % domain_size + 1)
    return picks


@dataclass
class SelectionReproductionRow:
    election_key: str
    county_level_match: str  # e.g. "63/63"
    statewide_match: str  # e.g. "1/1", or "0/0 (blocked)"


#: Table 2, reproduced from the paper (§5.2) as a reference value -- see
#: the module docstring for why the full multi-county sweep isn't rerun
#: here. Each cell is "matched/checkable"; "(blocked)" marks a known,
#: independently-detected manifest gap (§3.4) that prevents any
#: reproduction attempt from running at all for that cell.
TABLE_2: list[SelectionReproductionRow] = [
    SelectionReproductionRow("2019-statewide", "63/63", "1/1"),
    SelectionReproductionRow("2020-general", "61/63", "0/0 (blocked)"),
    SelectionReproductionRow("2020-presidential", "0/0 (blocked)", "0/0 (blocked)"),
    SelectionReproductionRow("2020-stateprimary", "88/88", "1/1"),
    SelectionReproductionRow("2021-coordinated", "62/64", "0/0 (blocked)"),
    SelectionReproductionRow("2022-primary", "78/80", "2/2"),
    SelectionReproductionRow("2022-general", "62/63", "0/6 (blocked)"),
    SelectionReproductionRow("2023-coordinated", "62/63", "1/1"),
    SelectionReproductionRow("2024-general", "62/63", "2/2"),
    SelectionReproductionRow("2025-coordinated", "72/73", "2/2"),
    SelectionReproductionRow("2026-primary", "112/112", "1/1"),
]


@dataclass
class TypedDiscrepancyValidationRow:
    o2: int
    o1: int
    u1: int
    u2: int
    total: int


#: Table 3, reproduced from the paper (§5.3) as a reference value: across
#: the 477 formally targeted contests, independently-derived counts
#: (scoped to each contest's own formal sample draw, preserving draw
#: multiplicity) match CORLA's own reported counts exactly. Reproducing
#: this scoping from cross_election.db alone requires the same
#: formal-sample identification machinery noted in the module docstring.
TABLE_3_CORLA_REPORTED = TypedDiscrepancyValidationRow(o2=18, o1=8, u1=12, u2=8, total=46)
TABLE_3_INDEPENDENTLY_DERIVED = TypedDiscrepancyValidationRow(o2=18, o1=8, u1=12, u2=8, total=46)
