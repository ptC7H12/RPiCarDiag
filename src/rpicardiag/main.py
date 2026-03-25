"""RPiCarDiag — entry point."""
from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="RPiCarDiag")
    parser.add_argument("--sim", action="store_true", help="Force simulation mode")
    parser.add_argument(
        "validate_config",
        nargs="?",
        metavar="validate-config",
        help="Validate a vehicle config YAML file",
    )
    parser.add_argument("config_path", nargs="?", help="Path to config file to validate")
    args = parser.parse_args()

    if args.validate_config == "validate-config" and args.config_path:
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
