"""pytest fixtures for RPiCarDiag tests."""
from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture
def sim_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force simulation mode regardless of platform."""
    monkeypatch.setenv("RPICARDIAG_SIM", "1")


@pytest.fixture
def sample_vehicle_config() -> dict[str, Any]:
    """Return a minimal valid vehicle config dict for unit tests."""
    return {
        "vehicle": {"name": "Test Vehicle", "protocol": "obd2"},
        "signals": [
            {
                "id": "0x0C",
                "name": "RPM",
                "category": "Motor",
                "start_bit": 0,
                "length": 16,
                "byte_order": "big_endian",
                "is_signed": False,
                "factor": 0.25,
                "offset": 0,
                "unit": "rpm",
            }
        ],
    }
