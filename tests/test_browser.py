import pytest
from app.browser import execute_steps
@pytest.mark.asyncio
async def test_host_allowlist():
    with pytest.raises(ValueError): await execute_steps("https://not-allowed.invalid",[],{"example.com"})
