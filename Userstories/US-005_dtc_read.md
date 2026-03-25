# US-005 — DTC Lesen

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: US-003, US-010

---

## Description
Als Techniker möchte ich gespeicherte Fehlercodes (DTCs) von einem oder mehreren Steuergeräten auslesen und mit Code, Beschreibung und Status (aktiv/gespeichert/ausstehend) angezeigt bekommen, damit ich Fahrzeugprobleme diagnostizieren kann.

## Acceptance Criteria
- [ ] Button "Fehlerspeicher auslesen" startet den Scan aller konfigurierten ECUs
- [ ] Jeder DTC wird angezeigt: Code (P/B/C/U + 4 Ziffern), Beschreibung, Status, betroffene ECU
- [ ] Status-Farben: aktiv = rot, gespeichert = orange, ausstehend = gelb
- [ ] Leerer Fehlerspeicher zeigt "Keine Fehler gefunden" mit grünem Indikator
- [ ] Scan-Fortschritt wird angezeigt (Spinner + ECU-Name)
- [ ] Letzter Scan-Zeitpunkt wird angezeigt
- [ ] DTC-Liste wird in SQLite gespeichert (für Export US-013)
- [ ] Freeze-Frame-Daten werden bei Verfügbarkeit pro DTC gespeichert
- [ ] Funktioniert in Simulation Mode (US-008) mit Dummy-DTCs

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/dtc_screen.py`
- DTC-Logik: `core/dtc_manager.py` (liest via python-obd oder UDS über CAN)
- Repository: `db/repositories/dtc_repository.py`
- Model: `models/dtc.py` (code, description, status: DtcStatus enum, ecu, freeze_frame: dict|None, timestamp)
- Widget: `ui/widgets/dtc_entry.py`
- Standard-OBD-II: Mode 03 (aktive DTCs), Mode 07 (ausstehende), Mode 0A (gespeicherte)
- Beschreibungs-Lookup: integrierte DTC-Datenbank (P0xxx SAE-Standard) + fahrzeugspezifische Erweiterungen in YAML

## Open Questions
- Soll auch ISO-14229 (UDS) für erweiterte Diagnose-Sessions unterstützt werden?
- OEM-spezifische DTC-Codes (P1xxx–P3xxx): Beschreibungen per YAML einpflegbar?
