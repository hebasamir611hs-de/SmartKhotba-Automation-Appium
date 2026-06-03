"""
DEPRECATED — SmartKhotba uses OTP verification, not username/password login.
See test_otp.py for phone/OTP verification tests.
"""
import pytest
from tests.base_test import BaseTest

pytestmark = pytest.mark.skip(reason="Login disabled — guest mode active")


class TestLogin(BaseTest):
    """Placeholder — auth is OTP-based, not credential-based."""
    pass
