"""Vehicle identification via VIN and ECU fingerprints.

Reads VIN (OBD2 Mode 09 PID 0x02 / UDS DID 0xF190) and ECU identification
data (DIDs 0xF187, 0xF189, 0xF197, 0xF18C) to auto-match the correct
vehicle config file from config/vehicles/.

Public API:
    read_vin(connection) -> str
        Read 17-char VIN from connected vehicle.

    read_ecu_info(connection) -> dict[str, str]
        Read standard ECU identification DIDs.

    scan_configs(config_dir: Path) -> list[dict]
        Load all vehicle configs and their identification blocks.

    match_config(vin: str, ecu_info: dict, configs: list) -> dict | None
        Match VIN/ECU info against configs, return best match or None.
"""
