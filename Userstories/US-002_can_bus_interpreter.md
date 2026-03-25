# US-002 — CAN Bus Interpreter

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: US-003, US-008, US-010

---

## Description
Als Techniker möchte ich CAN-Frames dekodiert als menschenlesbare Signalwerte sehen — mit Name, aktuellem Wert, Einheit und Beschreibung — organisiert in Kategorie-Tabs (z.B. Motor, Komfort, Sicherheit, Karosserie), damit ich schnell die relevanten Daten finde.

## Acceptance Criteria
- [ ] Signale werden aus rohen CAN-Frames per Fahrzeug-YAML dekodiert
- [ ] Anzeige: Signal-Name, aktueller Wert, Einheit, letztes Update (Timestamp)
- [ ] Tabs pro Kategorie (aus YAML-Feld `category`)
- [ ] Signale innerhalb einer Kategorie alphabetisch sortierbar
- [ ] Werte werden live aktualisiert (kein manuelles Refresh)
- [ ] Signale mit veralteten Werten (>5s kein Update) werden ausgegraut
- [ ] Suchfeld zum Filtern von Signalen über alle Kategorien
- [ ] Klick auf Signal → Detailansicht (Rohdaten, Skalierung, Bit-Position)
- [ ] Funktioniert in Simulation Mode (US-008)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/interpreter_screen.py`
- Dekodierung: `core/can_decoder.py` (parsed YAML-Config, extrahiert Bits, skaliert)
- Model: `models/decoded_signal.py` (name, value, unit, category, description, last_seen: float)
- Bit-Extraktion: `utils/can_utils.py` (start_bit, length, byte_order, is_signed, factor, offset)
- QTabWidget für Kategorien, QListView + QAbstractListModel für Signale pro Tab

## Open Questions
- Sollen Grenzwert-Warnungen (min/max aus YAML) farblich hervorgehoben werden?
- Soll der Interpreter auch Standard-OBD-II-PIDs (Mode 01) anzeigen, wenn kein Custom-YAML vorhanden?
