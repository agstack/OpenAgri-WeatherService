import pytest
from tests.fixtures import *

from src.utils import calculate_thi


class TestUtils:

    # Test calulation of THI
    @pytest.mark.anyio
    async def test_thi(self):
        # Test a typical case
        assert calculate_thi(30.0, 60.0) == 79.76
        # Test edge cases
        assert calculate_thi(14.5, 100) == 58.1
        assert calculate_thi(-10.0, 50.0) == 26.2
