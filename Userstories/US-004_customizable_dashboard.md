# US-004 — Customizable Dashboard

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: US-002, US-003, US-011

---

## Description
Als Fahrer/Techniker möchte ich Signale aus dem Interpreter per Dialog auf ein Dashboard-Raster ziehen und die Darstellungsform (Gauge, Balken, Zahlenwert) wählen, damit ich ein personalisiertes Cockpit-Display aufbauen kann. Das Layout soll pro Fahrzeugprofil gespeichert werden.

## Acceptance Criteria
- [ ] Dashboard zeigt ein frei belegbares Raster (z.B. 3×4 Tiles auf 7")
- [ ] "Widget hinzufügen"-Button öffnet Dialog: Signal auswählen + Darstellungsform wählen
- [ ] Darstellungsformen: Gauge (kreisförmig), Balken (horizontal), Zahlenwert (numerisch)
- [ ] Tiles zeigen Live-Werte aus dem Interpreter (via Qt-Signal)
- [ ] Tile löschen per Long-Press oder Kontextmenü
- [ ] Layout wird pro Fahrzeugprofil in SQLite gespeichert und beim nächsten Start wiederhergestellt
- [ ] Leeres Dashboard zeigt Hinweis "Kein Widget vorhanden — tippe '+' um anzufangen"
- [ ] Funktioniert in Simulation Mode (US-008)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/dashboard_screen.py`
- Tile-Widget: `ui/widgets/dashboard_tile.py` (Container für Gauge/Bar/Value)
- Gauge: `ui/widgets/signal_gauge.py`, Bar: `ui/widgets/signal_bar.py`, Value: `ui/widgets/signal_value.py`
- Dialog: `ui/dialogs/add_widget_dialog.py`
- Persistenz: `db/repositories/dashboard_repository.py` (SQLite: dashboard_layouts table)
- Model: `models/dashboard_widget.py` (signal_id, display_type, position: row/col, config)
- Touch Drag & Drop auf PyQt6: `QApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents)` + QDrag
- Achtung: Touch-DnD auf Qt erfordert expliziten Event-Filter — sorgfältig implementieren

## Open Questions
- Soll die Tile-Größe variabel sein (1×1, 1×2, 2×2)?
- Soll es vordefinierte Dashboard-Templates (z.B. "Motorsport", "Eco") geben?
