# Mercedes W447 / OM651 — DPF-Monitoring Referenz

Technische Referenz für das DPF-Echtzeit-Monitoring des OM651-Dieselmotors (Bosch EDC17C66) im Mercedes W447 (V-Klasse / Vito). Basiert auf verifizierten UDS-DIDs aus DTS Monaco, Vediamo und Community-Reverse-Engineering.

---

## UDS-Kommunikation

- **ECU**: Motorsteuergerät CRD3 (Bosch EDC17C66)
- **CAN-Bus**: CAN C (500 kbps)
- **UDS-Service**: 0x22 ReadDataByIdentifier
- **Session**: Default Session (0x01) — kein Extended Session oder Security Access nötig für Lese-DIDs
- **ISO-TP**: Standard-Adressierung über CAN C, Timing P2=50ms

---

## Verifizierte DIDs

### DPF-Hauptsignale

| DID | Signal | Bytes | Formel | Einheit | Bereich | Anmerkung |
|-----|--------|-------|--------|---------|---------|-----------|
| 0x0444 | DPF Füllstand | 2 (uint16) | raw / 7 | % | 0–300% | >100% = überladen |
| 0x0444 | DPF Rußmasse | 2 (uint16) | raw | g | 0–999 | Absolute Masse |
| 0x8018 | DPF Differenzdruck | 2 (uint16) | raw × 1.45 | mbar | 0–200 | Druckdifferenz über DPF |
| 0x8000 | Abgasgegendruck | 2 (uint16) | raw × 1.45 | mbar | 0–500 | Gesamt-Gegendruck |
| 0x2529 | Regen-Zähler | 2 (uint16) | raw | Anzahl | 0–9999 | Seit Werk / seit letztem Reset |

### Abgastemperaturen (Zehntel-Kelvin)

Alle Temperaturen werden als Zehntel-Kelvin übertragen: `°C = (raw - 2731) / 10`

Äquivalent in linearer Formel: `factor = 0.1, offset = -273.1`

| DID | Signal | Position | Normalbereich | Max. |
|-----|--------|----------|---------------|------|
| 0x8020 | AGT vor DPF | Nach Oxidations-Kat, vor Filter | 200–550°C | 700°C |
| 0x2961 | AGT vor Kat | Vor Oxidations-Kat (Turboauslass) | 150–500°C | 700°C |
| 0x2984 | AGT vor SCR | Nach DPF, vor SCR-Kat | 150–350°C | 600°C |
| 0x8E2C | AGT vor Turbo | Direkt am Krümmerausgang | 200–600°C | 800°C |

### Kontext-DIDs (Motor)

| DID | Signal | Formel | Einheit | Anmerkung |
|-----|--------|--------|---------|-----------|
| 0x8010 | Ladedruck | raw × 1.45 | mbar | Absolut |
| 0x8030 | Ladelufttemperatur | (raw-2731)/10 | °C | Nach Ladeluftkühler |
| 0x8032 | Motoröltemperatur | (raw-2731)/10 | °C | Betriebstemperatur ~90-110°C |
| 0x8060 | Kraftstofftemperatur | (raw-2731)/10 | °C | Einfluss auf Einspritzung |
| 0x8070 | Common-Rail-Druck | raw × 0.145 | bar | 200–2000 bar |
| 0xA482 | Ist-Drehmoment | raw | Nm | Aktuelles Motormoment |
| 0x8422 | AGR-Bypass | raw | — | Bypass-Klappenstellung |

### Kontext-DIDs (Fahrzeug)

| DID | Signal | Formel | Einheit | Anmerkung |
|-----|--------|--------|---------|-----------|
| 0x1414 | Tankfüllstand | raw × 2.65 | Liter | Verbrauchsüberwachung |
| 0x8028 | Umgebungstemperatur | (raw-2731)/10 | °C | Einfluss auf Regen-Strategie |
| 0xAC2E | Atmosphärendruck | raw × 1.45 | mbar | Höhenkorrektur |

---

## DPF-Regeneration

### Erkennung (Software-Logik)

Es gibt kein einzelnes DID für den Regenerationsstatus. Die Erkennung erfolgt über Signalkombination:

```
Regeneration aktiv WENN:
  AGT_vor_DPF > 550°C
  UND DPF_Füllstand(t) < DPF_Füllstand(t - 30s)   # sinkt

Zusätzliche Indikatoren:
  - Kraftstoffverbrauch ~2-3 L/h über Normal
  - AGR-Bypass öffnet sich
  - Ladedruck kann schwanken

Regeneration beendet WENN:
  AGT_vor_DPF < 400°C
  ODER DPF_Füllstand < 15%
```

### Regenerationsarten

| Typ | Auslöser | Temperatur | Dauer |
|-----|----------|-----------|-------|
| Passive Regen | Autobahn (>80 km/h, hohe Last) | 350–450°C | Kontinuierlich |
| Aktive Regen | ECU-gesteuert (Füllstand >80%) | 550–650°C | 15–30 min |
| Service-Regen | DTS Monaco / Vediamo (Werkstatt) | 600–700°C | 30–45 min |
| Notfall-Regen | Limp-Mode (Füllstand >160%) | — | Werkstatt nötig |

### Schwellwerte

| Füllstand | Stufe | Bedeutung |
|-----------|-------|-----------|
| 0–50% | Normal | Kein Handlungsbedarf |
| 50–90% | Erhöht | Nächste Regen wird bald gestartet |
| 90–100% | Warnung | Regenerationsfahrt empfohlen (Autobahn, 30 min) |
| 100–160% | Kritisch | Aktive Regen gescheitert, Werkstatt empfohlen |
| >160% | Notfall | Limp-Mode aktiv oder unmittelbar bevorstehend |

---

## DID-Scan-Methodik

### Bekannte DIDs verifizieren

```python
import isotp
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client

conn = IsoTPSocketConnection('can0', isotp.Address(
    isotp.AddressingMode.Normal_11bits,
    rxid=0x07E8,   # Motor-ECU Response
    txid=0x07E0    # Motor-ECU Request
))

known_dids = [0x0444, 0x8018, 0x8000, 0x8020, 0x2961, 0x2984, 0x8E2C, 0x2529]

with Client(conn) as client:
    for did in known_dids:
        try:
            resp = client.read_data_by_identifier(did)
            raw = resp.service_data.values[did]
            print(f"DID 0x{did:04X}: {raw.hex()} (raw={int.from_bytes(raw, 'big')})")
        except Exception as e:
            print(f"DID 0x{did:04X}: {e}")
```

### Neue DIDs entdecken (Brute-Force-Scan)

```python
# WARNUNG: Nur bei stehendem Fahrzeug, nie bei laufendem Motor!
for did in range(0x0000, 0xFFFF):
    try:
        resp = client.read_data_by_identifier(did)
        raw = resp.service_data.values[did]
        print(f"DID 0x{did:04X}: {raw.hex()}")
    except:
        pass
```

---

## Hardware-Empfehlungen

### Raspberry Pi CAN-Interface

| Option | Chip | Oszillator | CAN-Bus | Preis |
|--------|------|-----------|---------|-------|
| PiCAN 2 | MCP2515 | 16 MHz | 1× CAN | ~30€ |
| 2CH CAN HAT | MCP2515 ×2 | 8 MHz | 2× CAN | ~25€ |
| Waveshare RS485 CAN HAT | MCP2515 | 12 MHz | 1× CAN | ~15€ |
| USB: Innomaker USB2CAN | GS_USB | — | 1× CAN | ~25€ |

### Oszillator-Konfiguration

Der MCP2515 Oszillator muss in `/boot/config.txt` korrekt angegeben werden:

```bash
# PiCAN 2 (16 MHz)
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25

# 2CH CAN HAT (8 MHz)
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
dtoverlay=mcp2515-can1,oscillator=8000000,interrupt=24

# Waveshare (12 MHz)
dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25
```

### OBD-Kabel

Standard OBD-II zu DB9 Kabel (Pin 6 = CAN-H, Pin 14 = CAN-L). Kein Pegelwandler nötig — der MCP2515/TJA1050 auf den HATs übernimmt die CAN-Transceiver-Funktion.

---

## Quellen

| Quelle | Beschreibung |
|--------|-------------|
| DTS Monaco / Vediamo | Offizielle Mercedes Diagnose-DIDs (verifiziert) |
| MHH AUTO Forum | Community-verifizierte DID-Listen für OM651 |
| Motor-Talk | OM651 DPF-Erfahrungsberichte und Schwellwerte |
| Bosch EDC17 Dokumentation | ECU-interne Skalierungsformeln |
| SAE J1979 / ISO 15031-5 | Standard-OBD2-PIDs (Basis für 0x04xx DIDs) |
