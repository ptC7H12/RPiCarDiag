# US-001 — CAN Bus Sniffer

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: US-003, US-008, US-010

---

## Description
Als Techniker möchte ich eine live-scrollende Tabelle mit rohen CAN-Frames sehen (Arbitration-ID, DLC, Datenbytes, Timestamp), um den Bus-Traffic zu beobachten, ohne dekodierte Signal-Definitionen zu benötigen. Der Sniffer soll filterbar sein und einen Pause/Resume-Modus haben.

## Acceptance Criteria
- [ ] Tabelle zeigt CAN-Frames in Echtzeit (ID hex, DLC, 8 Byte hex, Timestamp ms)
- [ ] Neue Frames werden oben eingefügt (neueste zuerst), ältere scrollen nach unten
- [ ] Filter nach Arbitration-ID (hex-Eingabe, Wildcard *)
- [ ] Pause-Button friert die Anzeige ein, ohne den Buffer zu leeren
- [ ] Frame-Zähler und Bus-Last-Indikator in der Statusleiste
- [ ] Maximale Buffer-Größe konfigurierbar (default: 1000 Frames), älteste werden verworfen
- [ ] Anzahl verworfener Frames wird angezeigt
- [ ] Funktioniert in Simulation Mode (US-008)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/sniffer_screen.py`
- CAN-Daten kommen via Qt-Signal von `core/can_bus.py` (QThread)
- Widget-Row: `ui/widgets/can_frame_row.py`
- Model: `models/can_frame.py` (dataclass mit arbitration_id, dlc, data: bytes, timestamp: float)
- Ringbuffer in `core/can_bus.py` verhindert UI-Überlastung bei hoher Bus-Last (500kbps CAN = bis zu 3500 Frames/s)
- QTableView mit QAbstractTableModel für Performance (kein QTableWidget)

## Open Questions
- Soll Colorierung nach ID-Range möglich sein (z.B. Motor-IDs grün, Karosserie blau)?
- Hex-Dump oder auch binäre Darstellung der Datenbytes?
