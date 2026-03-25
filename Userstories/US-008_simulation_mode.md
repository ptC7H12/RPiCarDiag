# US-008 — Simulation Mode

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: —

---

## Description
Als Entwickler möchte ich die Anwendung auf einem Nicht-Pi-Entwicklungsrechner ohne CAN/OBD-Hardware mit einem virtuellen Bus und voraufgezeichneten Daten starten können, damit der gesamte Entwicklungs- und Test-Workflow unabhängig von physischer Hardware funktioniert.

## Acceptance Criteria
- [ ] `python -m rpicardiag --sim` startet im Sim-Mode auf jedem OS (Linux/macOS/Windows)
- [ ] Sim-Mode wird automatisch aktiviert, wenn kein `/dev/spidev0.0` (MCP2515) vorhanden ist
- [ ] Sim-Mode zeigt deutlichen Hinweis-Banner in der UI: "SIMULATION — keine echte Fahrzeugverbindung"
- [ ] Virtueller CAN-Bus liefert pre-recorded Frames aus einer `.asc`-Beispieldatei
- [ ] Simulierte DTCs sind in `config/sim/` als YAML definiert
- [ ] Alle Screens (Sniffer, Interpreter, Dashboard, DTC, Coding) funktionieren vollständig im Sim-Mode
- [ ] Sim-Mode kann auch für pytest-Tests verwendet werden (kein Hardware-Fixture nötig)

## Technical Notes
- Platform-Erkennung: `utils/platform_detect.py`
  - Prüft `/dev/spidev0.0` → SIM_MODE Flag
  - Prüft `--sim` CLI-Argument → SIM_MODE Flag erzwingen
- CAN-Bus: `core/can_bus.py` — wenn SIM_MODE: python-can `virtual` Bus + `.asc`-Replay via `can.LogReader`
- OBD: `core/obd_connection.py` — wenn SIM_MODE: lokale Dummy-Responses aus YAML
- Sim-Daten: `config/sim/sample_can_session.asc`, `config/sim/sample_dtcs.yaml`
- pytest conftest: `tests/conftest.py` exportiert `sim_can_bus` Fixture

## Open Questions
- Soll der Sim-Mode auch aufgezeichnete Sessions (US-009) als Eingabe nutzen können?
- Soll die Replay-Geschwindigkeit einstellbar sein (1×, 2×, 0.5×)?
