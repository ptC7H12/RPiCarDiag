# US-012 — Dark / Automotive Theme

**Status**: offen
**Priority**: High
**Step**: 1
**Depends on**: —

---

## Description
Als Fahrer möchte ich ein dunkles Hochkontrast-UI-Theme optimiert für den Fahrzeugeinsatz bei wechselnden Lichtverhältnissen, damit der 7"-Touchscreen sowohl bei direkter Sonneneinstrahlung als auch bei Nachtfahrten gut ablesbar ist.

## Acceptance Criteria
- [ ] Standard-Theme beim ersten Start ist Dark Mode (automotive-optimiert)
- [ ] Hintergrundfarbe: tiefschwarz (#0A0A0A), nicht grau
- [ ] Primärtext: hoher Kontrast (#F0F0F0), WCAG AA-konform (Kontrastverhältnis ≥ 4.5:1)
- [ ] Akzentfarben: systemische Farben für Status (grün = ok, gelb = warnung, rot = fehler/aktiv)
- [ ] Touch-Targets: alle interaktiven Elemente ≥ 48×48 px
- [ ] Schriftgröße M = 14pt (Standard auf 7"), L = 18pt
- [ ] Keine weißen oder hellen Flächen, die blenden könnten
- [ ] Signal-Werte in Gauge/Bar: leuchtende Akzentfarbe auf dunklem Hintergrund
- [ ] Light Theme verfügbar als Alternative (für indoor/workshop-Nutzung)
- [ ] Theme über QSS vollständig konfigurierbar (keine hardcodierten Farben im Python-Code)

## Technical Notes
- Styles: `src/rpicardiag/ui/styles/dark.qss` und `light.qss`
- Farb-Palette (Dark):
  ```
  Background:    #0A0A0A
  Surface:       #1A1A1A
  Primary text:  #F0F0F0
  Secondary:     #A0A0A0
  Accent:        #00B4D8  (blau für aktive Elemente)
  Success:       #2ECC71
  Warning:       #F39C12
  Error:         #E74C3C
  Border:        #2A2A2A
  ```
- Touch-Target-Enforcement via `setMinimumSize(48, 48)` in Basis-Widget-Klasse
- `main_window.py` lädt QSS via `QApplication.setStyleSheet()`
- Fonts: System-Font oder eingebettete Schrift (Roboto/Inter) für klare Lesbarkeit

## Open Questions
- Soll die Helligkeit der UI per Schieberegler anpassbar sein (Nacht-Dimm-Modus)?
- Soll die Akzentfarbe (Blau) konfigurierbar sein?
