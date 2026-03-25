# US-015 — DPF-Echtzeit-Monitor (Diesel-Partikelfilter)

**Status**: offen
**Priority**: Mittel
**Step**: 2
**Depends on**: US-002, US-003, US-014

---

## Description
Ein dedizierter DPF-Monitor-Screen zeigt den aktuellen Zustand des Diesel-Partikelfilters in Echtzeit an. Der Screen nutzt UDS-DIDs (Service 0x22) des OM651-Motorsteuergeräts, um Füllstand, Abgastemperaturen, Differenzdruck und Regenerationsstatus live darzustellen.

## Acceptance Criteria
- [ ] Dedizierter DPF-Screen mit Live-Werten: Füllstand (%), Differenzdruck, AGT vor/nach DPF
- [ ] Füllstands-Balken mit Farbcodierung: grün (<50%), gelb (50-90%), orange (90-100%), rot (>100%)
- [ ] Schwellwert-Alarme: 90% Warnung, 100% Kritisch, 200% Notfall (Limp-Mode-Gefahr)
- [ ] Regenerations-Erkennung: AGT vor DPF > 550°C UND DPF-Füllstand sinkt → "Regeneration aktiv" anzeigen
- [ ] Regenerations-History: Zähler (DID 0x2529), eigene Events mit Timestamp und km-Stand
- [ ] Abgastemperatur-Übersicht: vor Kat, vor DPF, vor SCR, vor Turbo — als Diagramm oder Zahlenwerte
- [ ] CSV-Export der DPF-Daten für Langzeit-Analyse
- [ ] Sim-Mode: simulierte DPF-Werte aus `config/sim/mercedes_w447_coding.yaml`
- [ ] Touch-optimiert (48x48px Targets, große Schrift für Werte)

## Technical Notes

### Verifizierte UDS-DIDs (OM651 / CRD3)

| Signal | DID | Formel | Einheit |
|--------|-----|--------|---------|
| DPF Füllstand | 0x0444 | raw / 7 | % |
| DPF Differenzdruck | 0x8018 | raw * 1.45 | mbar |
| Abgasgegendruck | 0x8000 | raw * 1.45 | mbar |
| AGT vor DPF | 0x8020 | (raw - 2731) / 10 | °C |
| AGT vor Kat | 0x2961 | (raw - 2731) / 10 | °C |
| AGT vor SCR | 0x2984 | (raw - 2731) / 10 | °C |
| AGT vor Turbo | 0x8E2C | (raw - 2731) / 10 | °C |
| Regen-Zähler | 0x2529 | raw | Anzahl |

Alle Formeln sind als `factor * raw + offset` abbildbar (siehe vehicle config).

### Regenerations-Erkennung

Logische Kombination (kein eigenes DID):
```
WENN  AGT_vor_DPF > 550°C
UND   DPF_Füllstand sinkt (Delta über 30s)
DANN  Regeneration = aktiv
```

Zusätzliche Indikatoren:
- Kraftstoffverbrauch steigt (~2-3 L/h über Normal)
- AGR-Bypass öffnet sich
- Ladedruck kann leicht schwanken

### Schwellwerte

| Füllstand | Stufe | Aktion |
|-----------|-------|--------|
| < 50% | Normal (grün) | — |
| 50–90% | Erhöht (gelb) | Info-Anzeige |
| 90–100% | Warnung (orange) | Warnung: "Regenerationsfahrt empfohlen" |
| 100–200% | Kritisch (rot) | Alarm: "DPF kritisch — sofortige Regeneration nötig" |
| > 200% | Notfall (rot blinkend) | Alarm: "Limp-Mode droht — Werkstatt aufsuchen" |

### Dateien
- UI: `src/rpicardiag/ui/screens/dpf_screen.py` (**neu**)
- Signale: `config/vehicles/mercedes_vklasse_w447.yaml` (Kategorie "DPF", "Abgastemperatur")
- Sim: `config/sim/mercedes_w447_coding.yaml` (DPF-DIDs)
- Referenz: `docs/mercedes_w447_dpf_reference.md`
