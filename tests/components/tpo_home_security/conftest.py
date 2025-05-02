"""Common fixtures for the home_sec tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.tpo_home_security.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry
