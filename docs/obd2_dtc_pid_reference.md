# OBD2 DTC & PID Referenzquellen

Übersicht externer Quellen für OBD2-Diagnosecodes (DTCs) und Parameter-IDs (PIDs), die für RPiCarDiag genutzt werden können.

---

## pyOBD 0.9.3

**Lizenz:** GPL v2
**Quelle:** www.obdtester.com
**Download:** `pyobd_0.9.3.tar.gz`

### Inhalt

| Datei | Inhalt | Anzahl |
|-------|--------|--------|
| `obd2_codes.py` | Diagnostic Trouble Codes als Python-Dict `pcodes` | 2.087 DTCs |
| `obd_sensors.py` | OBD2 Mode-01 PIDs mit Konvertierungsfunktionen | 32 PIDs |

### DTC-Aufschlüsselung

- **1.731 P-Codes** (Powertrain) — Motor, Getriebe, Antrieb
- **299 U-Codes** (Network) — Kommunikation zwischen Steuergeräten
- **0 B-Codes** (Body) — Karosserie, Komfort (nicht enthalten)
- **0 C-Codes** (Chassis) — Fahrwerk, ABS, ESP (nicht enthalten)

### DTC-Kategorien (aus `pcode_classes`)

| Bereich | Beschreibung |
|---------|-------------|
| P00XX | Fuel and Air Metering, Auxiliary Emission Controls |
| P01XX | Fuel and Air Metering |
| P02XX | Fuel and Air Metering |
| P03XX | Ignition System or Misfire |
| P04XX | Auxiliary Emission Controls |
| P05XX | Vehicle Speed, Idle Control, Auxiliary Inputs |
| P06XX | Computer and Auxiliary Outputs |
| P07XX–P09XX | Transmission |
| P0AXX | Hybrid Propulsion |
| P10XX–P19XX | Manufacturer Controlled (herstellerspezifisch) |

### OBD2 PIDs (Mode 01)

| PID | Name | Einheit | Formel |
|-----|------|---------|--------|
| 0100 | Supported PIDs | — | Bitstring |
| 0101 | Status Since DTC Cleared | — | Bitmuster |
| 0104 | Calculated Load Value | % | raw × 100 / 255 |
| 0105 | Coolant Temperature | °C | raw - 40 |
| 0106 | Short Term Fuel Trim | % | (raw - 128) × 100 / 128 |
| 0107 | Long Term Fuel Trim | % | (raw - 128) × 100 / 128 |
| 010B | Intake Manifold Pressure | psi | raw / 0.14504 |
| 010C | Engine RPM | rpm | raw / 4 |
| 010D | Vehicle Speed | MPH | raw / 1.609 |
| 010E | Timing Advance | degrees | (raw - 128) / 2 |
| 010F | Intake Air Temp | °C | raw - 40 |
| 0110 | Air Flow Rate (MAF) | lb/min | raw × 0.00132276 |
| 0111 | Throttle Position | % | raw × 100 / 255 |
| 011F | Time Since Engine Start | min | raw / 60 |

### Datenstruktur

```python
# obd2_codes.py — Struktur:
pcodes = {
    "P0001": "Fuel Volume Regulator Control Circuit/Open",
    "P0002": "Fuel Volume Regulator Control Circuit Range/Performance",
    # ... 2085 weitere Einträge
    "U0431": "Invalid Data Received From Body Control Module 'A'"
}

# obd_sensors.py — Struktur:
class Sensor:
    name: str           # "Engine RPM"
    cmd: str            # "010C"
    value: Callable     # Konvertierungsfunktion
    unit: str           # "rpm"
```

### Nutzung für RPiCarDiag

Die pyOBD-Daten sind GPL v2 lizenziert und werden **nicht direkt** ins Projekt kopiert. Stattdessen können sie als Referenz dienen:

1. **DTC-Lookup**: Die `pcodes`-Dict-Struktur kann als Vorlage für eine eigene DTC-Datenbank dienen
2. **PID-Formeln**: Die Konvertierungsfunktionen bestätigen die Standard-OBD2-Skalierungen
3. **Validation**: Gegen pyOBD-Daten prüfen, ob eigene DTC-Beschreibungen korrekt sind

---

## Alternative Quellen

### python-obd (bereits Dependency)

Die `python-obd` Bibliothek (MIT-Lizenz) enthält eine eigene DTC-Dekodierung und PID-Definitionen. Da sie bereits in den Projekt-Dependencies ist, kann sie direkt für DTC-Lookup genutzt werden:

```python
import obd
# DTC-Codes werden automatisch dekodiert
cmd = obd.commands.GET_DTC  # Mode 03
response = connection.query(cmd)
for dtc in response.value:
    print(f"{dtc.code}: {dtc.description}")
```

### SAE J2012 / ISO 15031-6

Der offizielle Standard für OBD2-Fehlercodes. Kostenpflichtig über SAE International. Enthält alle P/B/C/U-Codes mit offiziellen Beschreibungen.

### OpenDBC (commaai)

Open-Source CAN-DBC-Dateien für viele Fahrzeuge. Enthält Signal-Definitionen, aber keine DTC-Datenbank.
**GitHub:** github.com/commaai/opendbc

### Herstellerspezifische Codes

Für Mercedes-spezifische DTCs (P2xxx, P0xxx Erweiterungen) sind die CBF-Dateien die primäre Quelle. Siehe `docs/mercedes_w447_uds_reference.md` für Details zum CBF-Parsing.

---

## Einschränkungen

| Lücke | Beschreibung | Mögliche Quelle |
|-------|-------------|-----------------|
| B-Codes (Body) | Nicht in pyOBD enthalten | SAE J2012, herstellerspezifisch |
| C-Codes (Chassis) | Nicht in pyOBD enthalten | SAE J2012, herstellerspezifisch |
| Mercedes P2xxx | Herstellerspezifische Erweiterungen | CBF-Dateien (CaesarSuite) |
| Mode 06 Test-IDs | On-Board Monitoring Test Results | SAE J1979 |
| Freeze-Frame PIDs | Erweiterte Freeze-Frame-Daten | Fahrzeugspezifisch |
