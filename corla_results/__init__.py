"""Reproduce the tables and headline numbers in the accompanying paper
("paper.md") directly from cross_election.db.

Scope note, read this first: this package queries the *already
normalized* database bundled with this repository. It does not include
the separate pipeline that builds that database from the raw per-election
CORLA exports in the year directories alongside it (2017/ through 2026/)
-- that normalization pipeline is a substantially larger piece of the
underlying project, out of scope for this submission package. See
DATABASE.md for the schema and how each table traces back to specific
raw files.
"""

from . import coverage, discrepancies, verification

__all__ = ["coverage", "discrepancies", "verification"]
