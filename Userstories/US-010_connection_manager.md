# US-010 — Connection Manager

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: US-008

---

## Description
Als Benutzer möchte ich einen dedizierten Screen zur Auswahl des CAN/OBD-Adapter-Typs (MCP2515/socketcan, ELM327 USB, ELM327 Bluetooth), Konfiguration der Verbindungsparameter und Anzeige des Live-Verbindungsstatus, damit ich ohne YAML-Editierung zwischen Adapter-Typen wechseln kann.

## Acceptance Criteria
- [ ] Screen zeigt aktuellen Verbindungsstatus (Verbunden / Getrennt / Fehler) mit Farbindikator
- [ ] Adapter-Typ auswählbar: MCP2515 (socketcan), ELM327 USB, ELM327 Bluetooth
- [ ] Konfigurierbare Parameter je nach Typ:
  - MCP2515: Interface (can0/can1), Bitrate (125k/250k/500k/1M)
  - ELM327 USB: Port (/dev/ttyUSB0 etc.), Baudrate
  - ELM327 BT: Bluetooth-Gerät scannen und auswählen
- [ ] "Verbinden"-Button startet Verbindungsaufbau mit Spinner + Timeout (10s)
- [ ] "Trennen"-Button trennt sauber (Bus-Lifecycle in can_bus.py)
- [ ] Connection Badge in der Hauptnavigation zeigt Live-Status (US-012 konform)
- [ ] Verbindungsparameter werden in `app_config.yaml` gespeichert
- [ ] Verbindungsfehler zeigen klare Fehlermeldung (kein Stack-Trace dem Benutzer)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/connection_screen.py`
- Widget: `ui/widgets/connection_badge.py` (in main_window.py Navigationsleiste)
- Core: `core/can_bus.py` (adapter_type Parameter), `core/obd_connection.py`
- Config: `config/app_config.yaml` (adapter_type, interface, bitrate, port)
- ELM327 BT: `python-obd` unterstützt Bluetooth via `obd.Async(portstr='...')`
- MCP2515 Setup: `ip link set can0 type can bitrate 500000 && ip link set can0 up` (muss als root oder via sudoers laufen)
- Fehlerklassen in `core/can_bus.py`: `BusConnectionError`, `BusTimeoutError`

## Open Questions
- Soll automatisches Reconnect bei Verbindungsabbruch konfigurierbar sein?
- Soll der Bluetooth-Scan direkt in der App integriert werden oder auf System-BT-Einstellungen verweisen?
