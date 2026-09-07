"""Reproduces the paper's Tables 4 and 5 (§6: discrepancy typing and the
reconciliation-gap check).
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

# Elections excluded from the polished per-type breakdown (Table 4)
# because their underlying source files are documented (§6.4) as raw
# exports never further categorized by the state -- reporting a number
# for them without that qualification would be misleading. 2018 general
# and 2020 presidential are legitimately included (with real data);
# 2017/2018 primary have no comparison data of any kind and are simply
# absent from the elections table under this era filter.
_EXCLUDED_FROM_TABLE_4 = ("2019-statewide", "2022-general")


@dataclass
class DiscrepancyTypeRow:
    election_key: str
    o2: int
    o1: int
    u1: int
    u2: int
    total: int
    examined: int

    @property
    def rate(self) -> float:
        return self.total / self.examined if self.examined else 0.0


#: 2018 general is a known, documented exception (§6.4 of the paper):
#: it has only an aggregate, contest-level discrepancy-type count
#: available in the state's own original export (`contest_detail.csv`'s
#: own aggregate columns), not per-ballot `ballot_comparisons` rows --
#: this database does not carry that aggregate table, so this one row
#: cannot be re-derived from cross_election.db alone and is reproduced
#: here verbatim from the paper instead, exactly like Table 5's external
#: reference numbers.
_2018_GENERAL_ROW = DiscrepancyTypeRow(
    election_key="2018-general", o2=6, o1=3, u1=0, u2=3, total=12, examined=164_796
)


def discrepancy_types_by_election(conn: sqlite3.Connection) -> list[DiscrepancyTypeRow]:
    """One row per election: counts of each Kaplan-Markov discrepancy type
    (o2/o1/u1/u2) among genuine discrepancies, plus the total number of
    contest-ballot comparison rows examined ("Examined", the rate's
    denominator -- a contest-examination count, not a count of distinct
    physical ballots; see §6.1).
    """
    rows: list[DiscrepancyTypeRow] = [_2018_GENERAL_ROW]
    elections = conn.execute(
        "SELECT election_id, key FROM elections "
        "WHERE export_era IN ('contest_csv', 'ballot_list') "
        "ORDER BY year, election_type"
    ).fetchall()

    for election_id, key in elections:
        if key in _EXCLUDED_FROM_TABLE_4:
            continue
        examined = conn.execute(
            "SELECT COUNT(*) FROM ballot_comparisons WHERE election_id = ?",
            (election_id,),
        ).fetchone()[0]
        if examined == 0:
            continue  # ballot_list-era elections (2017, 2018 primary) have none
        counts = dict(
            conn.execute(
                "SELECT discrepancy_type, COUNT(*) FROM ballot_comparisons "
                "WHERE election_id = ? AND is_genuine_discrepancy = 1 "
                "GROUP BY discrepancy_type",
                (election_id,),
            ).fetchall()
        )
        o2, o1, u1, u2 = counts.get("o2", 0), counts.get("o1", 0), counts.get("u1", 0), counts.get("u2", 0)
        rows.append(
            DiscrepancyTypeRow(
                election_key=key, o2=o2, o1=o1, u1=u1, u2=u2,
                total=o2 + o1 + u1 + u2, examined=examined,
            )
        )
    return rows


def discrepancy_types_overall(conn: sqlite3.Connection) -> DiscrepancyTypeRow:
    """The "Overall" row at the bottom of Table 4."""
    rows = discrepancy_types_by_election(conn)
    return DiscrepancyTypeRow(
        election_key="Overall",
        o2=sum(r.o2 for r in rows), o1=sum(r.o1 for r in rows),
        u1=sum(r.u1 for r in rows), u2=sum(r.u2 for r in rows),
        total=sum(r.total for r in rows), examined=sum(r.examined for r in rows),
    )


@dataclass
class ReconciliationRow:
    election_key: str
    rederived: int
    previously_published: int

    @property
    def gap(self) -> int:
        return self.rederived - self.previously_published


#: The "previously published" side of Table 5 is an earlier, independently
#: produced tally of these same eight elections' reason-annotated
#: discrepancy reports -- a fixed external reference number, not derived
#: from this database, reproduced here verbatim from the paper (§6.4) for
#: the comparison. It cannot be recomputed from cross_election.db alone.
_PREVIOUSLY_PUBLISHED_TOTALS: dict[str, int] = {
    "2020-stateprimary": 122,
    "2020-general": 280,
    "2021-coordinated": 44,
    "2022-primary": 93,
    "2023-coordinated": 22,
    "2024-general": 235,
    "2025-coordinated": 22,
    "2026-primary": 16,
}


def reconciliation_by_election(conn: sqlite3.Connection) -> list[ReconciliationRow]:
    """One row per reason-annotated election: this database's own
    independently re-derived discrepancy-report row count (from
    `sos_discrepancy_report_rows`, the state's post-audit discrepancy
    report, ingested by this project's own importer) against the earlier
    published tally in `_PREVIOUSLY_PUBLISHED_TOTALS` (§6.4).
    """
    rows: list[ReconciliationRow] = []
    for key, published in _PREVIOUSLY_PUBLISHED_TOTALS.items():
        election_id = conn.execute(
            "SELECT election_id FROM elections WHERE key = ?", (key,)
        ).fetchone()
        if election_id is None:
            continue
        rederived = conn.execute(
            "SELECT COUNT(*) FROM sos_discrepancy_report_rows WHERE election_id = ?",
            (election_id[0],),
        ).fetchone()[0]
        rows.append(ReconciliationRow(key, rederived, published))
    return rows
