# Hardware Setup

## Required Hardware

- Raspberry Pi 4 or 5 (min. 2GB RAM)
- 7" DSI or HDMI Touchscreen
- MCP2515 CAN Bus Hat (SPI) **or** ELM327 USB/Bluetooth adapter
- OBD-II cable (for ELM327) or direct CAN wiring (for MCP2515)

## MCP2515 (SPI CAN Hat)

### `/boot/config.txt` entries:
```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25
dtoverlay=spi-bcm2835
```

### Bring up the CAN interface:
```bash
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
ip -details link show can0
```

Add to `/etc/network/interfaces` for automatic startup:
```
allow-hotplug can0
iface can0 can static
    bitrate 500000
```

## ELM327 USB

Plug in adapter, check port:
```bash
ls /dev/ttyUSB*
```

Set in `config/app_config.yaml`:
```yaml
adapter:
  type: elm327_usb
  port: /dev/ttyUSB0
```

## ELM327 Bluetooth

Pair via `bluetoothctl`, then connect via rfcomm:
```bash
sudo rfcomm connect /dev/rfcomm0 <BT_MAC_ADDRESS> 1
```

Set in `config/app_config.yaml`:
```yaml
adapter:
  type: elm327_bt
  port: /dev/rfcomm0
```

## Mercedes W447 — Besonderheiten

### CAN-Bus-Topologie

Der W447 nutzt drei separate CAN-Netzwerke, verbunden über ein Central Gateway (CGW) im SAM Front:

| CAN Bus | Geschwindigkeit | Funktion |
|---------|----------------|----------|
| CAN C | 500 kbps | Antrieb, Bremsen, Lenkung |
| CAN B | 250 kbps | Karosserie, Display, Beleuchtung |
| CAN D | 500 kbps | Diagnose (OBD-Port) |

**Wichtig:** Der OBD-Port verbindet nur mit CAN D. Das CGW routet Diagnoseanfragen zum internen CAN-Bus. Lesen aller CAN-Frames ist möglich, Schreiben nur von Diagnose-CAN-IDs.

### MCP2515 Konfiguration für W447

```
# /boot/config.txt — 16 MHz Oszillator für PiCAN 2:
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
```

```bash
# CAN-Interface für W447 CAN D (500 kbps):
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
```

### Verbindung testen

```bash
# CAN-Traffic mitlesen:
candump can0

# Diagnose-Request senden (Tester Present):
cansend can0 0639#3E00

# Alle Frames eines ECUs filtern (z.B. IC Response-ID 0x0641):
candump can0,0641:07FF
```

### UDS über ISO-TP

Für UDS-Kommunikation wird ISO-TP (ISO 15765-2) als Transport Layer benötigt. Die Python-Libraries `udsoncan` und `can-isotp` übernehmen dies automatisch. Details und Code-Beispiele: siehe `docs/mercedes_w447_uds_reference.md`.

## Touchscreen Calibration (7" DSI)

For official Raspberry Pi 7" display no extra config is needed.
For third-party displays, install `xinput-calibrator` and run:
```bash
xinput_calibrator
```
