# Architecture

## Layer Model

```
┌─────────────────────────────────────────┐
│               UI Layer                  │
│   PyQt6 Screens / Widgets / Dialogs     │
│   Subscribes to Qt-Signals only         │
└───────────────────┬─────────────────────┘
                    │ Qt-Signals
┌───────────────────▼─────────────────────┐
│              Core Layer                 │
│   can_bus  obd_conn  dtc_mgr  decoder   │
│   Runs in QThread, emits Qt-Signals     │
└───────────┬───────────────┬─────────────┘
            │               │
┌───────────▼───┐   ┌───────▼─────────────┐
│  Models Layer │   │     DB Layer        │
│  Dataclasses  │   │  SQLite via repos   │
└───────────────┘   └─────────────────────┘
            │
┌───────────▼─────────────────────────────┐
│           Config Layer                  │
│  YAML loading + schema validation       │
└───────────┬─────────────────────────────┘
            │
┌───────────▼─────────────────────────────┐
│          Hardware Layer                 │
│  MCP2515/socketcan  ELM327  sim-mode    │
└─────────────────────────────────────────┘
```

## Threading

- Main thread: PyQt6 event loop
- `CanBusThread(QThread)`: reads from hardware, emits `frame_received(CanFrame)` signal
- All UI updates happen in main thread via signal/slot connections

## Simulation Mode

`platform_detect.py` sets `SIM_MODE=True` if:
- `--sim` CLI flag passed, OR
- `/dev/spidev0.0` not found (not on a Pi), OR
- `RPICARDIAG_SIM=1` env variable set

In SIM_MODE: `can_bus.py` replays `config/sim/sample_can_session.asc` via `python-can` `virtual` bus.
