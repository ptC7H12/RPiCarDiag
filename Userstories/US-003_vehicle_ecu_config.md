# US-003 — Multi-Vehicle / ECU Config

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: —

---

## Description
Als Entwickler/Benutzer möchte ich fahrzeugspezifische CAN-IDs, Signal-Bit-Positionen, Skalierungsfaktoren und ECU-Adressen in separaten YAML-Dateien definieren, damit das Tool mehrere Fahrzeuge ohne Code-Änderungen unterstützt und die Community eigene Configs beitragen kann.

## Acceptance Criteria
- [ ] Pro Fahrzeug/ECU eine YAML-Datei unter `config/vehicles/`
- [ ] YAML-Format enthält: Fahrzeugname, Signals (ID, Bit-Position, Länge, Faktor, Offset, Einheit, Name, Kategorie, Beschreibung), ECU-Adressen
- [ ] Schema-Validierung bei App-Start gegen `config/schema/vehicle_config.schema.yaml`
- [ ] Ungültige Config → Fehlerdialog + Fallback auf `generic_obd2.yaml`
- [ ] `generic_obd2.yaml` enthält alle Standard-OBD-II-PIDs (Mode 01–09)
- [ ] CLI-Befehl zur Validierung: `python -m rpicardiag validate-config <path>`
- [ ] Fahrzeugprofil im Settings Screen (US-011) auswählbar
- [ ] Aktives Profil wird in `app_config.yaml` gespeichert

## Technical Notes
- Config-Loader: `src/rpicardiag/config/vehicle_config.py`
- Schema-Validator: `src/rpicardiag/config/schema_validator.py`
- Schema-Referenz: `config/schema/vehicle_config.schema.yaml`
- Beispiel-YAML: `config/vehicles/vw_golf_mk7.yaml`, `config/vehicles/generic_obd2.yaml`
- Model: `models/vehicle.py` (VehicleProfile dataclass)
- Signal-Definition im YAML:
  ```yaml
  signals:
    - id: "0x0C"          # OBD PID oder CAN-ID
      name: "Motordrehzahl"
      start_bit: 0
      length: 16
      byte_order: "big_endian"
      is_signed: false
      factor: 0.25
      offset: 0
      unit: "rpm"
      category: "Motor"
      description: "Aktuelle Motordrehzahl"
      min: 0
      max: 8000
  ```

## Open Questions
- Soll ein GUI-Editor für Vehicle-YAMLs integriert werden (spätere Story)?
- Format für Multi-ECU-Support: ein YAML pro ECU oder alle ECUs in einer Fahrzeug-Datei?
