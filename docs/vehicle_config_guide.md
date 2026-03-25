# Vehicle Config Guide

Vehicle-specific data (CAN IDs, signal definitions, ECU addresses, coding options)
is defined in YAML files under `config/vehicles/`.

## Creating a new vehicle config

```bash
cp config/vehicles/generic_obd2.yaml config/vehicles/my_car.yaml
# Edit my_car.yaml with your vehicle's specifics
python -m rpicardiag validate-config config/vehicles/my_car.yaml
```

## YAML structure

```yaml
vehicle:
  name: "My Car Model"
  protocol: "can"          # obd2 | can | uds
  year_from: 2018
  year_to: 2023

ecus:
  - name: "Engine ECU"
    address: "0x7E0"
    response_address: "0x7E8"

signals:
  - id: "0x280"            # CAN ID (hex) or OBD PID
    name: "Engine RPM"
    category: "Motor"      # Groups signals into tabs
    description: "Engine speed"
    start_bit: 16          # bit position within CAN frame
    length: 16             # number of bits
    byte_order: "big_endian"
    is_signed: false
    factor: 0.25           # physical = raw * factor + offset
    offset: 0
    unit: "rpm"
    min: 0
    max: 8000

coding:                    # Optional: variant coding entries
  - id: "my_feature"
    name: "My Feature"
    ecu: "Engine ECU"
    address: "0x0042"
    bit: 3
    description: "Enables my feature"
    values:
      0: "disabled"
      1: "enabled"
```

## Finding CAN IDs for your vehicle

1. Use the CAN Bus Sniffer (US-001) to observe raw traffic
2. Correlate frame IDs with actions (e.g., press accelerator, watch for changing frames)
3. Use online resources like OpenDBC, CSS Electronics database, or vehicle-specific forums
4. Document reverse-engineered signals in your vehicle YAML
