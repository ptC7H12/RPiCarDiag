"""DTC Manager — reading, clearing, and looking up diagnostic trouble codes.

Handles OBD-II Modes 03 (active DTCs), 07 (pending), 0A (stored)
and UDS Service 0x19 (ReadDTCInformation).

To be implemented: see US-005 (DTC Lesen) and US-006 (DTC Löschen).
"""

from __future__ import annotations


def lookup_dtc(code: str) -> str | None:
    """Look up a DTC description by its code (e.g. "P0300").

    Returns the human-readable description, or None if unknown.

    This is an interface stub. A DTC database must be provided externally.
    Options:
      - python-obd library (MIT, already in dependencies) — use obd.commands.GET_DTC
      - Custom YAML/JSON database under config/dtc/
      - pyOBD 0.9.3 (GPL v2, external) — 2087 codes, see docs/obd2_dtc_pid_reference.md

    For manufacturer-specific codes (Mercedes P2xxx etc.), parse CBF files
    with CaesarSuite — see docs/mercedes_w447_uds_reference.md.
    """
    # TODO: Implement with chosen DTC data source
    return None
