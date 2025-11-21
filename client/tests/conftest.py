"""
Pytest configuration for multi-agent earnings analyzer tests.

This module configures pytest fixtures and settings for the test suite.
"""

import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the path to the test data directory"""
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def sample_earnings_report(test_data_dir):
    """Return the path to the sample earnings report"""
    report_path = test_data_dir / "earnings_report_sample.txt"
    if report_path.exists():
        return str(report_path)
    return None
