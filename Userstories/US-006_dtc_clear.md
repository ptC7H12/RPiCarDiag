# US-006 — DTC Löschen

**Status**: offen
**Priority**: Medium
**Step**: 2
**Depends on**: US-005

---

## Description
Als Techniker möchte ich gespeicherte Fehlercodes eines ausgewählten Steuergeräts nach expliziter Bestätigung eines Warndialogs löschen können, damit ich den Fehlerspeicher nach einer Reparatur zurücksetzen kann.

## Acceptance Criteria
- [ ] "Fehlerspeicher löschen"-Button ist nur aktiv, wenn DTCs vorhanden und eine ECU ausgewählt ist
- [ ] Bestätigungsdialog mit Warnung: "Dies löscht alle gespeicherten Fehler. Nicht rückgängig zu machen."
- [ ] Nach Bestätigung: OBD Mode 04 / UDS ClearDiagnosticInformation wird gesendet
- [ ] Erfolgsmeldung + automatischer Re-Scan nach dem Löschen
- [ ] Fehlgeschlagene Löschung zeigt Fehlermeldung mit Details
- [ ] Löschvorgang wird mit Timestamp in SQLite protokolliert
- [ ] Nicht möglich während aktiver Fahrt (Warnung wenn Fahrzeug bewegt wird, optional via Geschwindigkeits-Signal)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/dtc_screen.py` (erweiterung von US-005)
- Logik: `core/dtc_manager.py` — Zwei-Schritt-Pattern:
  1. `dtc_manager.request_clear(ecu)` → gibt `ClearRequest`-Objekt zurück
  2. `dtc_manager.confirm_clear(request)` → führt aus (erst nach Dialog-Bestätigung aufrufbar)
- Dialog: `ui/dialogs/confirm_dialog.py`
- OBD-II: `python-obd` Command `CLEAR_DTC`
- Protokollierung in `db/repositories/dtc_repository.py`

## Open Questions
- Soll selektives Löschen pro DTC unterstützt werden (falls ECU das unterstützt)?
- Löschen nur bei Zündung an oder auch bei abgestelltem Motor?
