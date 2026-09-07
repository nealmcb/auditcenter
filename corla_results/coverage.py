"""Reproduces the paper's Table 1 (contest coverage classification, §4).

Classifies every contest in the normalized dataset by (a) how CORLA's own
export names it -- directly targeted, opportunistically named, or no
comparison record at all -- and (b) how many counties its own ballot
population spans -- single-county, partial multi-county, or statewide.
See §4.1 of the paper for the full definitions.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass
class ElectionCoverageRow:
    election_key: str
    total_contests: int
    directly_targeted: int
    opportunistically_named: int
    no_comparison_record: int
    single_county: int
    partial_multi_county: int
    statewide: int


# The three earliest-era elections (2017, 2018 primary, 2018 general's
# first three rounds) never populate a per-contest parameter file at all
# -- only manifest-level data -- so they cannot be classified by this
# method (§4.1) and are excluded here, not counted as zero.
_EARLIEST_ERA_ELECTION_KEYS = ("2017", "2018-primary")


def coverage_by_election(conn: sqlite3.Connection) -> list[ElectionCoverageRow]:
    """Return one row per election, reproducing Table 1's columns.

    `coverage_status` values are 'targeted', 'opportunistic_covered',
    'fragmented_only', or 'zero_coverage'. 'fragmented_only' contests
    (real risk_calculations data exists, but no true-contest-level
    comparison row was ever consolidated under the bare/canonical name)
    count toward "no comparison record" here, matching the paper's own
    §4.1 definition: CORLA's own export never names the contest by its
    true, consolidated identity, only under a raw county-suffixed
    fragment name.
    """
    elections = conn.execute(
        "SELECT election_id, key FROM elections "
        "WHERE export_era = 'contest_csv' ORDER BY year, election_type"
    ).fetchall()

    rows: list[ElectionCoverageRow] = []
    for election_id, key in elections:
        if key in _EARLIEST_ERA_ELECTION_KEYS:
            continue

        total_counties = conn.execute(
            "SELECT COUNT(*) FROM county_manifests WHERE election_id = ?",
            (election_id,),
        ).fetchone()[0]

        contest_rows = conn.execute(
            "SELECT true_contest_id, coverage_status FROM true_contests "
            "WHERE election_id = ?",
            (election_id,),
        ).fetchall()

        directly_targeted = opportunistic = no_record = 0
        single = partial = statewide = 0
        for true_contest_id, status in contest_rows:
            if status == "targeted":
                directly_targeted += 1
            elif status == "opportunistic_covered":
                opportunistic += 1
            elif status in ("zero_coverage", "fragmented_only"):
                no_record += 1

            county_count = conn.execute(
                "SELECT COUNT(DISTINCT county_key) FROM contest_counties "
                "WHERE election_id = ? AND true_contest_id = ?",
                (election_id, true_contest_id),
            ).fetchone()[0]
            if county_count == 0:
                continue
            elif county_count == 1:
                single += 1
            elif total_counties and county_count >= total_counties:
                statewide += 1
            else:
                partial += 1

        rows.append(
            ElectionCoverageRow(
                election_key=key,
                total_contests=len(contest_rows),
                directly_targeted=directly_targeted,
                opportunistically_named=opportunistic,
                no_comparison_record=no_record,
                single_county=single,
                partial_multi_county=partial,
                statewide=statewide,
            )
        )
    return rows


def coverage_totals(conn: sqlite3.Connection) -> ElectionCoverageRow:
    """The "Total" row at the bottom of Table 1."""
    rows = coverage_by_election(conn)
    return ElectionCoverageRow(
        election_key="Total",
        total_contests=sum(r.total_contests for r in rows),
        directly_targeted=sum(r.directly_targeted for r in rows),
        opportunistically_named=sum(r.opportunistically_named for r in rows),
        no_comparison_record=sum(r.no_comparison_record for r in rows),
        single_county=sum(r.single_county for r in rows),
        partial_multi_county=sum(r.partial_multi_county for r in rows),
        statewide=sum(r.statewide for r in rows),
    )
