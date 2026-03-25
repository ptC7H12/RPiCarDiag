# Development Setup

## Requirements

- Python 3.11+
- Git

## Setup

```bash
git clone <repo>
cd RPiCarDiag
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
pip install -r requirements-dev.txt
```

## Run in Simulation Mode (no hardware needed)

```bash
python -m rpicardiag --sim
```

Simulation mode is also auto-detected: if `/dev/spidev0.0` is absent
(i.e., you are not on a Raspberry Pi), sim mode activates automatically.

## Run Tests

```bash
pytest tests/
pytest tests/unit/              # unit tests only
pytest tests/ui/ -v             # UI tests (requires display or xvfb)
```

For headless UI tests:
```bash
sudo apt install xvfb
xvfb-run pytest tests/ui/
```

## Linting

```bash
ruff check src/
ruff format src/
mypy src/
```

## Validate a vehicle config

```bash
python -m rpicardiag validate-config config/vehicles/my_car.yaml
```

## Project structure

See `todo.md` for the full project structure and coding rules.
