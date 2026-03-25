# US-009 — Session Logging & Replay

**Status**: offen
**Priority**: Medium
**Step**: 1
**Depends on**: US-008, US-010

---

## Description
Als Techniker möchte ich CAN- und OBD-Daten optional in eine timestamped Session-Datei aufzeichnen und gespeicherte Sessions später im Sniffer/Interpreter wiedergeben können, um intermittierende Fehler zu einem späteren Zeitpunkt offline zu analysieren.

## Acceptance Criteria
- [ ] "Aufzeichnung starten/stoppen"-Button im Sniffer und Interpreter Screen
- [ ] Aufzeichnung speichert alle CAN-Frames mit Timestamp in SQLite (Session-Tabelle)
- [ ] Aufzeichnungsstatus wird deutlich in der Statusleiste angezeigt (rotes "REC"-Symbol)
- [ ] Session-Liste zeigt alle gespeicherten Sessions: Datum, Dauer, Fahrzeugprofil, Frame-Anzahl
- [ ] "Wiedergeben"-Button für eine Session: Sniffer/Interpreter werden mit Session-Daten gespeist
- [ ] Wiedergabe-Geschwindigkeit einstellbar (0.5×, 1×, 2×, 5×, Max)
- [ ] Wiedergabe zeigt deutlichen Hinweis-Banner: "REPLAY — [Session-Name]"
- [ ] Sessions können exportiert werden (.asc-Format für externe Tools wie CANalyzer)
- [ ] Sessions können gelöscht werden (mit Bestätigung)

## Technical Notes
- Logger: `core/session_logger.py` (subscribt auf can_bus Qt-Signal, schreibt in DB)
- Repository: `db/repositories/session_repository.py`
- DB-Schema: `db/migrations/001_initial_schema.sql` (Tabellen: sessions, can_frames)
- Replay-Player: `core/can_bus.py` — Replay-Modus liest aus Session-Repository und emittiert Frames mit korrekten Delays
- `.asc`-Export via python-can `can.ASCWriter`
- Screen: Session-Liste als Dialog oder separater Tab im Settings Screen

## Open Questions
- Soll automatisches Logging bei Verbindungsaufbau konfigurierbar sein?
- Maximale Session-Dauer / Größe begrenzen (z.B. max 1 Stunde oder 100MB)?
