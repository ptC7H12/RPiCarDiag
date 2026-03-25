# US-014 — Automatische Fahrzeugerkennung

**Status**: offen
**Priority**: Hoch
**Step**: 1
**Depends on**: US-003, US-010

---

## Description
Beim Verbindungsaufbau liest das System die VIN (Fahrzeugidentifikationsnummer) und ECU-Identifikationsdaten automatisch aus und matcht die passende Vehicle-Config aus `config/vehicles/`. So entfällt die manuelle Auswahl des Fahrzeugprofils.

## Acceptance Criteria
- [ ] VIN wird automatisch beim Verbindungsaufbau gelesen (OBD2 Mode 09 PID 0x02 oder UDS DID 0xF190)
- [ ] VIN wird gegen `identification.vin_pattern` aller Vehicle-Configs gematcht
- [ ] Bei eindeutigem Match: Config automatisch laden, User wird informiert
- [ ] Bei mehreren Matches: Auswahldialog mit passenden Configs anzeigen
- [ ] Bei keinem Match: Fallback auf `generic_obd2_fallback`, Warnung anzeigen
- [ ] Optional: ECU-Fingerprint (DID 0xF197 System Name) als sekundäres Matching
- [ ] Erkannte VIN + ECU-Info wird in Session-Log geschrieben
- [ ] Im Sim-Mode: simulierte VIN aus sim-Config verwenden
- [ ] Manuelle Profilauswahl bleibt weiterhin möglich (Override)

## Technical Notes

### VIN-Lesung
- **OBD2**: Mode 09, PID 0x02 — Multi-Frame ISO-TP Response (17 ASCII-Zeichen)
- **UDS**: Service 0x22, DID 0xF190 — Response: `62 F1 90 [17 bytes ASCII]`
- Kein Security Access nötig für VIN-Abfrage (standardisiert)

### VIN-Struktur (ISO 3779)
| Position | Inhalt | Beispiel W447 |
|----------|--------|---------------|
| 1–3 | WMI (Weltherstellercode) | `WDF` = Mercedes-Benz Vans |
| 4 | Fahrzeugart | `4` = Vito/V-Klasse |
| 5–6 | Baureihe | `47` = W447 |
| 10 | Modelljahr | `F`=2015, `G`=2016, `H`=2017 |

### ECU-Identifikation (sekundär)
Standardisierte UDS-DIDs für ECU-Fingerprinting:
```
0xF187 — Spare Part Number (Teilenummer)
0xF189 — ECU Software Version
0xF18A — System Supplier (Bosch, Continental...)
0xF197 — System Name / Engine Type (z.B. "OM651")
0xF18C — ECU Serial Number
```

### Matching-Algorithmus
1. VIN lesen (OBD2 oder UDS)
2. Alle `config/vehicles/*.yaml` laden
3. Für jede Config mit `identification.vin_pattern`: Regex gegen VIN prüfen
4. Bei Match: Score berechnen (VIN-Pattern-Spezifität + ECU-Fingerprint-Matches)
5. Config ohne `identification`-Block = Fallback (niedrigste Priorität)

### Dateien
- Logik: `src/rpicardiag/core/vehicle_identifier.py` (**neu**)
  - `read_vin(connection) → str` — VIN auslesen (17 Zeichen)
  - `read_ecu_info(connection) → dict[str, str]` — ECU-DIDs lesen
  - `scan_configs(config_dir) → list[VehicleConfig]` — Alle Configs laden
  - `match_config(vin, ecu_info, configs) → VehicleConfig | None` — Bestes Match finden
- YAML: `vehicle.identification` Block in Vehicle-Configs (Schema erweitert)
- Sim: `config/sim/mercedes_w447_coding.yaml` enthält simulierte VIN-Responses

### Beispiel VIN-Matching
```python
# VIN: WDF4474011F123456
# → WMI: "WDF" (Mercedes Vans)
# → Baureihe: "447" (W447)
# → Matches: config/vehicles/mercedes_vklasse_w447.yaml
#   (vin_pattern: "^WDF447.*" ✓)
```
