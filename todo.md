# RPiCarDiag — Projektübersicht

Ein touch-optimiertes OBD/CAN-Diagnosetool für Raspberry Pi 4/5 mit 7" Touchscreen. Zielgruppe: KFZ-Techniker und Automotive-Enthusiasten. Das Tool ermöglicht CAN-Bus-Analyse, ECU-Fehlerdiagnose, Variantenkodierung und ein konfigurierbares Dashboard — vollständig über YAML-Configs fahrzeugspezifisch anpassbar.

---

## Tech Stack

| Layer | Technologie |
|---|---|
| Sprache | Python 3.11+ |
| UI | PyQt6 6.6+ |
| CAN | python-can 4.x (socketcan/MCP2515, virtual bus) |
| OBD-II | python-obd 0.7.x (ELM327 USB/BT) |
| Config | YAML (PyYAML 6.x), schema-validiert |
| Datenbank | SQLite (stdlib sqlite3) |
| Testing | pytest + pytest-qt |
| Linting | ruff + mypy |

---

## Features

### Step 1
- CAN Bus Sniffer (Rohdaten-Live-Ansicht)
- CAN Bus Interpreter (dekodierte Signale, kategorisiert)
- Multi-Vehicle / ECU Config (YAML pro Fahrzeug/ECU)
- Customizable Dashboard (Widgets per Drag & Drop)
- DTC Lesen (Fehlerspeicher auslesen)

### Step 2
- DTC Löschen (mit Bestätigungsdialog)
- Variantenkodierung (ECU-spezifische Sequences per YAML)

### Infrastruktur / Quer
- Simulation Mode (ohne Hardware entwickeln)
- Session Logging & Replay
- Connection Manager (Adapter-Auswahl)
- Settings Screen
- Dark/Automotive Theme
- Export Diagnostic Report

---

## Projektstruktur

```
RPiCarDiag/
├── todo.md / userstories.md / Userstories/
├── config/           # YAML: app_config, vehicles/, schema/
├── src/rpicardiag/   # Quellcode
│   ├── core/         # CAN, OBD, DTC, Decoder, Coder, Logger
│   ├── config/       # Config-Loader + Schema-Validator
│   ├── models/       # Dataclasses
│   ├── db/           # SQLite + Repositories + Migrations
│   ├── ui/           # Screens, Widgets, Dialogs, Styles
│   └── utils/        # Hilfsfunktionen, Platform-Detect
├── tests/            # unit/, integration/, ui/
└── docs/             # Architektur, Hardware-Setup, Guides
```

---

## Architektur-Prinzip

```
Hardware → Core (QThread) → Models → DB → UI
```

- UI berührt niemals Hardware direkt — alles über Qt-Signals
- Core-Module emittieren Qt-Signals, UI subscribt
- Config-Layer wird immer gegen Schema validiert
- Sim-Mode muss jederzeit funktionieren (kein Hardware-Zwang)

---

## Coding-Regeln

- Formatierung: `ruff format` (keine manuellen Ausnahmen)
- Typen: `mypy --strict` (alle public APIs vollständig typisiert)
- Kein `bare except:` — immer spezifische Exception fangen
- Keine hardcodierten IDs, Adressen oder Fahrzeugwerte — alles in YAML
- Alle destruktiven Operationen (DTC löschen, Coding schreiben) erfordern zwingend einen Bestätigungsdialog
- Simulation Mode muss nach jeder Änderung lauffähig bleiben
- Touch-Targets: Mindestgröße 48×48 px (WCAG Touch Guidelines)
- Jede neue Userstory bekommt eine eigene Datei in `Userstories/`

---

## Userstory-Regeln

- Wenn ein Kunde eine Story ändert: entsprechende `Userstories/US-XXX.md` anpassen
- Status immer aktuell halten: `offen` → `umgesetzt` → `nicht geplant`
- Neue Features → neue Story anlegen + `userstories.md` aktualisieren
- Änderungen an der Projektstruktur → diese Datei (`todo.md`) anpassen

---

## Dev Workflow

```bash
# Sim-Mode (ohne Hardware):
python -m rpicardiag --sim

# Tests:
pytest tests/

# Linting:
ruff check src/ && mypy src/

# Neues Fahrzeug-Config anlegen:
cp config/vehicles/generic_obd2.yaml config/vehicles/mein_auto.yaml
# → Felder anpassen, gegen Schema validieren:
python -m rpicardiag validate-config config/vehicles/mein_auto.yaml
```
