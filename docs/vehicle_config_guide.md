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
  manufacturer: "vw"       # optional: manufacturer identifier
  platform: "MQB"          # optional: platform code

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

## CAN Topology (multi-bus vehicles)

Vehicles with multiple CAN networks (e.g. Mercedes, BMW) can define their bus topology:

```yaml
can_topology:
  gateway: "SAM Front (CGW)"    # ECU acting as central gateway
  obd_port_bus: "CAN_D"         # which bus the OBD port connects to
  buses:
    - name: "CAN_C"
      bitrate: 500000
      description: "Engine/Chassis"
    - name: "CAN_B"
      bitrate: 250000
      description: "Interior/Body"
```

## ECU definitions (extended)

For UDS-based vehicles, ECUs support additional fields:

```yaml
ecus:
  - name: "Instrument Cluster"
    address: "0x0641"           # UDS address
    response_address: "0x0649"
    tx_id: "0x0639"             # CAN arbitration ID for requests
    rx_id: "0x0641"             # CAN arbitration ID for responses
    can_bus: "CAN_B"            # which CAN bus
    protocol: "uds"             # uds | kwp2000 | obd2
    cbf_file: "IC447KIG1"       # Mercedes CBF file reference
    description: "Continental NEC V850"
    security_access:
      coding_level: 0x0B        # Security Access level for coding
      coding_level_response: 0x0C
      seed_key_method: "mbseedkey"  # none | static | mbseedkey
```

## Variant coding

Two coding models are supported:

### Simple bit-level coding (e.g. VW)

Direct address + bit position within ECU coding space:

```yaml
coding:
  - id: "cornering_lights"
    name: "Cornering Lights"
    ecu: "BCM"
    address: "0x0042"
    bit: 3
    values:
      0: "disabled"
      1: "enabled"
```

### UDS DID-based coding (e.g. Mercedes)

Read/modify/write via UDS Data Identifiers (Services 0x22/0x2E):

```yaml
coding:
  - id: "restreichweite"
    name: "Range Display"
    ecu: "Instrument Cluster"
    did: "0x0108"               # UDS Data Identifier
    byte_offset: 0              # byte position in DID payload
    bit_offset: 1               # bit position within the byte
    bit_mask: "0x02"            # hex bitmask
    bit_length: 1               # number of bits
    data_type: "bit"            # bit | byte | integer | enum
    security_level: 0           # required Security Access level (0 = none)
    session_type: 0x03          # UDS session: 0x03 = extended
    requires_reset: true        # ECU reset after write?
    coding_group: "VCD_Variantencodierung"  # VCD group from CBF
    values:
      0: "disabled"
      1: "enabled"
    notes: "Confirmed raw UDS bytes: 0x30 → 0x32 (OR with 0x02)"
```

UDS coding flow: Extended Session (`10 03`) → Security Access (`27 XX`) → Read DID (`22 XX XX`) → Modify bits → Write DID (`2E XX XX [data] [fingerprint]`) → ECU Reset (`11 01`).

See `docs/mercedes_w447_uds_reference.md` for a complete Mercedes W447 example.

## Finding CAN IDs for your vehicle

1. Use the CAN Bus Sniffer (US-001) to observe raw traffic
2. Correlate frame IDs with actions (e.g., press accelerator, watch for changing frames)
3. Use online resources like OpenDBC, CSS Electronics database, or vehicle-specific forums
4. For Mercedes: parse CBF files with [CaesarSuite](https://github.com/jglim/CaesarSuite) to extract CAN IDs and parameter mappings
5. Document reverse-engineered signals in your vehicle YAML
