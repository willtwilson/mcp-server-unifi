import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ensure scripts/ is on the path so main.py can import unifi.transport
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))


@pytest.fixture
def mock_transport(monkeypatch):
    """Replace module-level _transport with a mock for isolation."""
    import main

    transport = MagicMock()
    transport.paginate.return_value = []
    transport.request.return_value = {}
    monkeypatch.setattr(main, "_transport", transport)
    return transport
