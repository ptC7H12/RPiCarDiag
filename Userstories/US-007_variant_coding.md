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
- [ ] UDS-Session-Management: Extended Session, Security Access, Tester Present
- [ ] Batch-Coding: mehrere Parameter einer ECU in einer Session schreiben

## Technical Notes

### Screen & Logik
- Screen: `src/rpicardiag/ui/screens/coding_screen.py`
- Logik: `core/variant_coder.py`
  - `read_coding(ecu_addr)` → aktuellen Wert lesen
  - `prepare_write(coding_id, new_value)` → `CodingRequest`-Objekt (kein Schreiben)
  - `execute_write(request)` → erst nach Bestätigung aufrufbar, schreibt Backup zuerst
- Dialog: `ui/dialogs/coding_confirm_dialog.py`
- Protokollierung: `db/repositories/dtc_repository.py` (Tabelle `coding_log`)

### UDS Coding-Flow (ISO 14229)

```
1. DiagnosticSessionControl (0x10 0x03) → Extended Session
2. SecurityAccess (0x27 [level]) → Seed/Key Austausch
3. ReadDataByIdentifier (0x22 [DID]) → Aktuellen Coding-String lesen
4. Bits/Bytes im Coding-String modifizieren
5. WriteDataByIdentifier (0x2E [DID] [data] [fingerprint]) → Schreiben
6. ECUReset (0x11 0x01) → Parameter neu laden
```

- **Tester Present** (`3E 00`) als Keep-Alive während Multi-Step-Operationen
- **Mercedes-spezifisch:** Coding-Payload = `[coding_bytes] + [4-Byte fingerprint]`

### Zwei Coding-Modelle

**Modell A — Einfache Bit-Kodierung (z.B. VW):**
```yaml
coding:
  - id: "cornering_lights"
    name: "Kurvenlicht"
    ecu: "Komfortsteuergerät"
    address: "0x0042"
    bit: 3
    values:
      0: "deaktiviert"
      1: "aktiviert"
```

**Modell B — UDS DID-basierte Kodierung (z.B. Mercedes):**
```yaml
coding:
  - id: "restreichweite"
    name: "Restreichweite"
    ecu: "Kombiinstrument (IC)"
    did: "0x0108"
    byte_offset: 0
    bit_offset: 1
    bit_mask: "0x02"
    bit_length: 1
    data_type: "bit"
    security_level: 0
    session_type: 0x03
    requires_reset: true
    values:
      0: "deaktiviert"
      1: "aktiviert"
```

### Dependencies
- `udsoncan` — UDS ISO 14229 Client
- `can-isotp` — ISO 15765-2 Transport Layer
- `python-can` — CAN-Bus Interface

### Referenz-Fahrzeug
Mercedes W447 V250 (2015 pre-facelift) — siehe `docs/mercedes_w447_uds_reference.md`

## Answered Questions

### Unterstützte Protokolle
**UDS (ISO 14229)** als primäres Protokoll. KWP2000 (ISO 14230) als Stretch Goal für ältere ECUs (z.B. Mercedes VGS4NAG2 Getriebe nutzt KW2C3PE).

### Batch-Coding
**Ja.** Zusammengehörige Parameter einer ECU können in einer Session geschrieben werden, ohne die Session zwischen jedem Parameter neu aufzubauen. Die Session wird mit Tester Present (`3E 00`) gehalten.

### Security Access (Service 27)
Seed/Key-Methode wird **pro ECU in YAML** konfiguriert:
```yaml
ecus:
  - name: "SAM Front"
    security_access:
      coding_level: 0x0B       # Security Level für Variant Coding
      seed_key_method: "mbseedkey"  # Algorithmus
      seed_key_dll: "CBC447.dll"    # DLL-Referenz (optional)
```
Unterstützte Methoden: `none` (kein SA nötig), `static` (fester Key), `mbseedkey` (Mercedes DLL-basiert).
