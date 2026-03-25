# Mercedes W447 V250 — UDS Coding Reference

Technische Referenz für die UDS-Variantenkodierung des Mercedes W447 (V-Klasse / Vito, 2015 pre-facelift). Basiert auf Community-verifizierten Daten von MHH AUTO, Digital Eliteboard, Motor-Talk und Open-Source-Projekten (CaesarSuite).

---

## CAN-Bus-Architektur

Der W447 nutzt **drei CAN-Netzwerke**, verbunden über ein Central Gateway (CGW) im SAM Front:

| CAN Bus | Geschwindigkeit | Funktion | ECUs |
|---------|----------------|----------|------|
| **CAN C** (Engine/Chassis) | 500 kbps | Antrieb, Bremsen, Lenkung | CRD3/MED40 (Motor), VGS4NAG2 (Getriebe), ESP9LEI, EPS218 |
| **CAN B** (Interior/Body) | 83.3–250 kbps | Karosserie, Display, Beleuchtung | IC447KIG1/KIG2, CBC447, ORC166, HU5, HVAC447 |
| **CAN D** (Diagnostic) | 500 kbps | OBD-Port → CGW | Pins 6 & 14 am OBD-II Stecker |

**Wichtig:** Mercedes nutzt **proprietäre CAN-IDs** (~0x0300–0x06xx), nicht die Standard-UDS-IDs (0x7DF–0x7E7). Die Response-ID liegt typischerweise bei Request-ID +0x08. Der OBD-Port verbindet nur mit CAN D; das CGW routet Diagnoseanfragen zum internen CAN-Bus.

---

## ECU-Map

| ECU | CBF-Datei | Funktion | CAN Bus | Protokoll |
|-----|-----------|----------|---------|-----------|
| Kombiinstrument (IC) | `IC447KIG1` / `IC447KIG2` | Tacho, Display, Warnungen | CAN B | UDS |
| SAM Front (CBC) | `CBC447` / `CB447` | Beleuchtung, Wischer, Verriegelung | CAN B | UDS |
| SAM Hinten | `SAMR_212` | Heckbeleuchtung, Sensoren | CAN B | UDS |
| EIS (Zündschloss) | `EIS447` | Wegfahrsperre, Schlüssel | CAN B+C | KW2C3PE/UDS |
| Motor (Diesel OM651) | `CRD3` / `CRD3S2` | Motorsteuerung (Bosch EDC17C66) | CAN C | UDS |
| Motor (Benzin M274) | `MED40` | Motorsteuerung | CAN C | UDS |
| Getriebe (7G-TRONIC) | `VGS4NAG2` | Automatikgetriebe | CAN C | KW2C3PE |
| ESP/ABS | `ESP9LEI` | ABS, ESP, Traktion | CAN C | UDS |
| Airbag | `ORC166` | Airbag, Gurtüberwachung | CAN B | UDS |
| COMAND NTG5 | `HU5` / `Audio447` | Navigation / Audio | CAN B + MOST | UDS |
| Klimaanlage | `HVAC447` | Klimasteuerung | CAN B + LIN | UDS |
| Reifendruck (TPMS) | `TPM3V1` | Reifendruckkontrolle | CAN B | UDS |
| Gateway | `HGW447` | High-Speed Gateway | CAN C + D | UDS |

---

## UDS-Protokoll: Coding-Ablauf

### Session-Sequenz

| Schritt | UDS Service | Bytes | Zweck |
|---------|-------------|-------|-------|
| 1. Extended Session | `0x10` DiagnosticSessionControl | `10 03` → `50 03 00 14 00 C8` | Erweiterte Diagnose-Session |
| 2. Security Access | `0x27` SecurityAccess | `27 0B` → `67 0B [seed]` → `27 0C [key]` → `67 0C` | ECU für Coding freischalten |
| 3. Kodierung lesen | `0x22` ReadDataByIdentifier | `22 [DID_hi] [DID_lo]` → `62 [DID_hi] [DID_lo] [data...]` | Aktuellen Coding-String lesen |
| 4. Kodierung schreiben | `0x2E` WriteDataByIdentifier | `2E [DID_hi] [DID_lo] [data...] [fingerprint]` → `6E [DID_hi] [DID_lo]` | Modifizierte Kodierung schreiben |
| 5. ECU Reset | `0x11` ECUReset | `11 01` → `51 01` | ECU-Parameter neu laden |
| 6. Tester Present | `0x3E` (Keep-Alive) | `3E 00` → `7E 00` | Session während Multi-Step-Ops halten |

### Security Access Levels

| Level | Request/Response | Verwendung |
|-------|-----------------|------------|
| 0x01 / 0x02 | `27 01` / `27 02` | Standard-Login |
| 0x0B / 0x0C | `27 0B` / `27 0C` | Variant Coding (die meisten ECUs) |
| 0x09 / 0x0A | `27 09` / `27 0A` | EEPROM-Zugang (IC AMG-Modifikationen) |

Seed-Key-Berechnung erfordert DLLs aus SMR-D-Dateien. Open-Source-Tool: [MBSeedKey](https://github.com/Xplatforms/mbseedkey).

### Coding-String-Struktur

Der Schreib-Payload für Service `0x2E` besteht aus:

```
[Variant Coding Datenbytes] + [4-Byte Fingerprint] + [opt. 16-Byte SCN]
```

- Factory-Fingerprint: `00 40 33 10`
- Vediamo-Fingerprint: `00 00 01 00`

### Standard-DIDs

| DID | Befehl | Inhalt |
|-----|--------|--------|
| `0xF100` | `22 F1 00` | Aktive Diagnose-Varianten-ID |
| `0xF151` | `22 F1 51` | Software-Version |
| `0xF154` | `22 F1 54` | Hardware-Info |
| `0xF190` | `22 F1 90` | VIN (17 ASCII-Zeichen) |
| `0xF804` | `22 F8 04` | Kalibrierung / SCN-Identifikation |
| `0x0108` | `22 01 08` | IC-Kodierung (bestätigt für Restreichweite) |

---

## Bestätigte Coding-Parameter

### Restreichweite (Reichweitenanzeige) — IC447KIG1

**Status: RAW UDS BYTES BESTÄTIGT**

| Schritt | Befehl | Beschreibung |
|---------|--------|-------------|
| Lesen | `22 01 08` | Read DID 0x0108 |
| Response | `62 01 08 30 00` | Byte 0 = `30` → Reichweite deaktiviert |
| Modifizieren | Bit 1 (Maske `0x02`) setzen | `30` → `32` (OR mit 0x02) |
| Schreiben | `2E 01 08 32 00` | Modifizierte Kodierung schreiben |
| Bestätigung | `6E 01 08` | Positive Response = Erfolg |

**Kein Security Access nötig** für diesen DID. Zündung nach Schreiben aus/ein.

### Tippblinken — CBC447 / CB447

**Status: COMMUNITY-BESTÄTIGT**

Community-Verifizierung von MHH AUTO (CB447 V-Klasse):
> "Done! now it is working. My car comes with CB447 samfront (class V). I was able to change longstring using Complete Vehicle Coding, replacing 03 by 05."

| Detail | Wert |
|--------|------|
| CBF | CB447 / CBC447 |
| VCD-Gruppe | `VCD_Parameter_Fahrtrichtungsanzeiger` |
| Parameter | `Tippblinken_Anzahl` |
| Kodierung | Direkter Integer-Byte-Wert: `0x03` = 3x → `0x05` = 5x |

### Weitere IC-Parameter (IC447KIG1)

| Parameter | VCD-Gruppe | Werte |
|-----------|-----------|-------|
| Zeigerwischen | `VCD_Variantencodierung` | `Vorhanden` / `Nicht_Vorhanden` |
| Reifendruck-Einheit | `VCD_Aktuelle_Menueeinstellungen` | `bar` / `PSI` / `kPa` |
| Gurtwarner | `VCD_Aktuelle_Menueeinstellungen` | 0=aus, 1=Euro-NCAP, 2=USA alt, 4=Euro-NCAP+Beifahrer |
| AMG-Menü | `VCD_06_Menueaktivierung` | Erfordert Security Level 0x09 + ggf. FW-Flash |

### SAM Front Parameter (CBC447)

| Funktion | VCD-Gruppe | Parameter | Standard → Ziel |
|----------|-----------|-----------|-----------------|
| TFL Skandinavien | `VCD_Parameter_Tagfahrlicht` | `PLSM_STL_mit_TFL` | `nicht_aktiv` → `aktiv` |
| Auffindbeleuchtung + Abblendlicht | `VCD_Parameter_Auffindbeleuchtung` | `Auffindbeleuchtung_mit_Abblendlicht` | `nicht_aktiv` → `aktiv` |
| Innenraumlicht bei Türöffnung | `VCD_Parameter_Auffindbeleuchtung` | `Innenraumbeleuchtung_bei_Tueroeffnung` | `aktiv` → `nicht_aktiv` |
| Orientierungslicht Dauer | `VCD_Parameter_Auffindbeleuchtung` | `Laufzeit_Orientierungslicht` | 10s/20s/30s/60s |
| Verriegelungs-Blinkimpulse | `VCD_Parameter_Verriegelungsquittierung` | `Blinkimpulse_Verriegelung` | 1–4+ |

**Hinweis:** Nach jeder SAM-Kodierung `DL_EEPROM_Schreiben` + `FN_HardReset` ausführen.

### ECO Start/Stop Deaktivierung

Drei Methoden, nach Zuverlässigkeit sortiert:

1. **CGW (zuverlässigste):** CGW CBF → Variant Coding → `Start/Stop` = `nicht_verfügbar`. Keine Warnlampen.
2. **Motor-ECU "Last Mode":** CRD3/MED40 → `Stopp-Start Standard Logik` = `Last Mode`. Merkt sich Button-Status.
3. **SAM Front:** Parameter `BC_F222` in der Fahrer-SAM-Kodierung (nicht bei allen Baujahren).

---

## Raspberry Pi SocketCAN Setup

### Hardware-Konfiguration

```bash
# /boot/config.txt für MCP2515 PiCAN 2:
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25

# CAN-Interface mit 500 kbps aktivieren:
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0
```

### Python-Stack

```
python-can (CAN-Bus Interface)
    → can-isotp (ISO 15765-2 Transport Layer)
        → udsoncan (ISO 14229 UDS Application Layer)
```

### Beispiel: Restreichweite aktivieren

```python
import isotp
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client

# CAN-IDs aus CBF oder Bus-Sniffing ermitteln
conn = IsoTPSocketConnection(
    'can0',
    isotp.Address(
        isotp.AddressingMode.Normal_11bits,
        rxid=0x0641,   # IC Response CAN ID
        txid=0x0639    # IC Request CAN ID
    )
)

with Client(conn, request_timeout=5) as client:
    client.change_session(0x03)  # Extended Session

    # Restreichweite lesen (DID 0x0108)
    resp = client.read_data_by_identifier(0x0108)
    current = bytearray(resp.service_data.values[0x0108])
    print(f"Aktuell: {current.hex()}")

    # Bit 1 setzen → Reichweite aktivieren
    current[0] |= 0x02

    # Schreiben
    client.write_data_by_identifier(0x0108, bytes(current))

    # ECU Reset
    client.ecu_reset(0x01)
```

### CAN-IDs ermitteln

Die exakten CAN Arbitration-ID-Paare (Request/Response) sind in den CBF-Dateien eingebettet:

1. **CBF parsen** mit [CaesarSuite](https://github.com/jglim/CaesarSuite) — `Trafo` konvertiert CBF → JSON
2. **CAN-Bus sniffen** während Vediamo/DTS Monaco kommuniziert: `candump can0`

---

## CBF-Dateien

CBF-Dateien (proprietäre Daimler-Binärdateien) definieren die vollständige Zuordnung:
- Parameter-Name → DID-Nummer → Byte-Offset → Bit-Maske → Enum-Werte
- Diagnose-Services (Request/Response-Bytes)
- Kommunikationsparameter (CAN-IDs, Baudraten, ISO-TP-Config)
- Eingebettete oder referenzierte Seed-Key-DLLs

**Pfad in Xentry:** `C:\Program Files (x86)\Mercedes-Benz\Xentry\MB_PKW\Caesar\cbf\`

**Open-Source-Tools:**
- [CaesarSuite](https://github.com/jglim/CaesarSuite) (MIT) — CBF→JSON Extraktion, Diogenes (experimenteller FOSS-Vediamo-Ersatz)
- [openStar](https://github.com/rnd-ash/openStar) — Rust-basierter FOSS Xentry/DAS-Ersatz mit SocketCAN
- [odxtools](https://github.com/mercedes-benz/odxtools) (MIT, offiziell von Mercedes) — ODX/PDX Parser für neuere Plattformen

---

## Quellen

| Quelle | Beschreibung |
|--------|-------------|
| MHH AUTO | DTS Monaco/Vediamo Coding Guide (6.000+ Seiten), bestätigte W447-Daten |
| Digital Eliteboard | Deutsche W447 Vediamo/DTS Monaco Anleitungen |
| Motor-Talk / Benzsport | "Der W447 und seine Optionen" — Übersicht aller codierbaren Funktionen |
| Codierschmiede.at | PDF mit allen W447 Coding-Möglichkeiten nach ECU |
| CaesarSuite (GitHub) | CBF-Parsing, Byte-Level Extraktion |
| OpenVehicleDiag / openStar (GitHub) | FOSS Diagnose-Tools mit CBF-Parsing und SocketCAN |
