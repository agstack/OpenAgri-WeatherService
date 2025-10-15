"""
Pytest configuration and shared fixtures for all tests.
This file is automatically loaded by pytest.
"""
import pytest

# Configure pytest-asyncio
@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests"""
    return 'asyncio'


# Configuration for pytest markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

