# US-007 — Variantenkodierung

**Status**: offen
**Priority**: Medium
**Step**: 2
**Depends on**: US-003, US-010

---

## Description
Als Entwickler/Techniker möchte ich fahrzeugspezifische ECU-Coding-Sequenzen (aus YAML-Config definiert) senden, um das Steuergerät-Verhalten zu modifizieren — mit obligatorischem Bestätigungsschritt und automatischem Backup des aktuellen Kodierungswerts vor dem Schreiben.

## Acceptance Criteria
- [ ] Coding-Screen listet alle verfügbaren Kodierungsoptionen aus der aktiven Vehicle-YAML
- [ ] Pro Option: Name, Beschreibung, aktueller Wert (aus ECU ausgelesen), verfügbare Werte/Bits
- [ ] "Kodierung lesen" liest aktuelle Werte aus den konfigurierten ECUs
- [ ] Änderung eines Werts öffnet Bestätigungsdialog mit explizitem Warnhinweis
- [ ] Vor dem Schreiben: aktueller ECU-Wert wird in SQLite gesichert ("Coding Backup")
- [ ] "Originalwert wiederherstellen"-Funktion aus dem Backup (pro Coding-Eintrag)
- [ ] Schreibvorgang wird mit Timestamp, ECU, alter/neuer Wert protokolliert
- [ ] Sequenz-Timeout: falls ECU nicht antwortet, Abbruch mit Fehlermeldung (kein Hang)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/coding_screen.py`
- Logik: `core/variant_coder.py`
  - `read_coding(ecu_addr)` → aktuellen Wert lesen
  - `prepare_write(coding_id, new_value)` → `CodingRequest`-Objekt (kein Schreiben)
  - `execute_write(request)` → erst nach Bestätigung aufrufbar, schreibt Backup zuerst
- Dialog: `ui/dialogs/coding_confirm_dialog.py`
- YAML-Struktur:
  ```yaml
  coding:
    - id: "cornering_lights"
      name: "Kurvenlicht"
      ecu: "BCM"
      service: "27"   # UDS service
      address: "0x0042"
      bit: 3
      description: "Aktiviert das dynamische Kurvenlicht"
      values:
        0: "deaktiviert"
        1: "aktiviert"
  ```
- Protokollierung: `db/repositories/dtc_repository.py` (eigene Tabelle `coding_log`)

## Open Questions
- Unterstützte Protokolle: nur UDS (ISO 14229) oder auch KWP2000 (ISO 14230)?
- Soll ein "Batch-Coding"-Modus mehrere Optionen in einer Session schreiben?
- Sicherheitszugang (Security Access, Service 27): Seed/Key-Algorithmus fahrzeugspezifisch in YAML?
