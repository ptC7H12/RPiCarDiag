# US-011 — Settings Screen

**Status**: offen
**Priority**: Medium
**Step**: 1
**Depends on**: US-003, US-008

---

## Description
Als Benutzer möchte ich einen Einstellungsscreen zur Auswahl des aktiven Fahrzeugprofils, UI-Präferenzen (Theme, Schriftgröße, Touch-Empfindlichkeit) und Logging-Optionen, damit ich das Tool ohne Konfigurationsdatei-Editierung anpassen kann.

## Acceptance Criteria
- [ ] Fahrzeugprofil: Dropdown mit allen YAMLs aus `config/vehicles/`, Reload-Button
- [ ] Theme: Dark / Light auswählbar (live preview), Neustartfrei anwendbar
- [ ] Schriftgröße: S / M / L (Mindestgröße M = 14pt für Touch-Bedienung)
- [ ] Logging: Auto-Log bei Verbindungsaufbau ein/aus, Max-Session-Größe (MB)
- [ ] Sprache: Deutsch / Englisch (Basis-Implementierung, erweiterbar)
- [ ] "Zurücksetzen auf Standard"-Button mit Bestätigung
- [ ] Alle Einstellungen sofort persistiert in `app_config.yaml`
- [ ] Änderungen wirken sich auf alle laufenden Screens aus (Qt-Signal `settings_changed`)

## Technical Notes
- Screen: `src/rpicardiag/ui/screens/settings_screen.py`
- Config: `src/rpicardiag/config/app_settings.py` (lädt/schreibt `config/app_config.yaml`)
- Theme-Wechsel: `main_window.py` lädt `ui/styles/dark.qss` oder `ui/styles/light.qss` via `app.setStyleSheet()`
- `app_config.yaml` Struktur:
  ```yaml
  active_vehicle: "generic_obd2"
  theme: "dark"
  font_size: "M"
  language: "de"
  logging:
    auto_log: false
    max_session_size_mb: 100
  adapter:
    type: "sim"
    interface: "can0"
    bitrate: 500000
  ```

## Open Questions
- Soll ein PIN-Schutz für destruktive Einstellungen (Coding, DTC löschen) konfigurierbar sein?
