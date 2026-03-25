"""RPiCarDiag — entry point."""
from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="RPiCarDiag — OBD/CAN Diagnostic Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Default: run the app
    parser.add_argument("--sim", action="store_true", help="Force simulation mode")

    # Subcommand: validate-config
    validate_parser = subparsers.add_parser(
        "validate-config", help="Validate a vehicle config YAML file"
    )
    validate_parser.add_argument("config_path", help="Path to config file to validate")

    args = parser.parse_args()

    if args.command == "validate-config":
        _validate_config(args.config_path)
        return

    _run_app(sim=args.sim)


def _validate_config(path: str) -> None:
    # TODO: implement via config.schema_validator
    print(f"Validating: {path}")
    print("Schema validation not yet implemented.")


def _run_app(sim: bool = False) -> None:
    # TODO: initialise PyQt6 QApplication, load config, start MainWindow
    print(f"RPiCarDiag starting (sim={sim}) — UI not yet implemented.")
    sys.exit(0)


if __name__ == "__main__":
    main()
