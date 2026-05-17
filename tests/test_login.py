"""
DEPRECATED — SmartKhotba uses OTP verification, not username/password login.
See test_otp.py for phone/OTP verification tests.
"""
import pytest
pytestmark = pytest.mark.skip(reason="Login disabled — guest mode active")
# This file intentionally left empty.
# Login tests have been moved to test_otp.py since the app
# uses phone number + OTP for authentication, not credentials.
