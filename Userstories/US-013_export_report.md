# US-013 — Export Diagnostic Report

**Status**: offen
**Priority**: Low
**Step**: 2
**Depends on**: US-005, US-009

---

## Description
Als Techniker oder Fahrzeugbesitzer möchte ich einen Diagnosebericht (DTC-Liste, Signal-Snapshot, Session-Zusammenfassung) als PDF oder Textdatei exportieren, um ihn an eine Werkstatt weiterzugeben oder für eigene Aufzeichnungen zu archivieren.

## Acceptance Criteria
- [ ] "Export"-Button im DTC-Screen und auf dem Dashboard
- [ ] Export-Formate: PDF und Plain Text (.txt)
- [ ] Bericht enthält: Fahrzeugprofil, Datum/Uhrzeit, DTC-Liste (Code, Beschreibung, Status), Signal-Snapshot (aktuelle Interpreter-Werte)
- [ ] Optional: Session-Zusammenfassung (Dauer, Frame-Anzahl, aufgetretene DTCs)
- [ ] Export-Speicherort: `/home/pi/rpicardiag_exports/` (konfigurierbar)
- [ ] Erfolgs-Toast zeigt Dateiname und Pfad
- [ ] Export-Datei kann auf USB-Stick gespeichert werden (falls gemountet)

## Technical Notes
- Export-Logik: `utils/report_exporter.py` (neu)
- PDF-Erzeugung: `reportlab` oder `fpdf2` (leichtgewichtig, kein LaTeX nötig)
- Dateiname-Muster: `rpicardiag_[FAHRZEUG]_[DATUM]_[UHRZEIT].[ext]`
- USB-Erkennung: `/media/pi/` mountpoint prüfen
- Daten-Quellen: `dtc_repository.py` + aktueller Interpreter-State

## Open Questions
- Soll ein QR-Code im PDF enthalten sein (z.B. Link zu DTC-Beschreibung)?
- Soll der Report per E-Mail versendbar sein (erfordert WLAN + SMTP-Konfig)?
