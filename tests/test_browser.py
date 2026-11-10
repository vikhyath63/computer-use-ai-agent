import asyncio
import pytest
from app.browser import execute_steps

def test_host_allowlist():
    with pytest.raises(ValueError):
        asyncio.run(execute_steps("https://not-allowed.invalid", [], {"example.com"}))
