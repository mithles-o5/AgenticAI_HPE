import pytest
from adapters.plugins.ipmi_adapter import IPMIAdapter

def test_ipmi_password_masking():
    creds = {
        "host": "10.0.0.1",
        "username": "admin",
        "password": "secretPassword123",
        "interface": "lanplus"
    }
    adapter = IPMIAdapter(creds)
    
    cmd = ["ipmitool", "-I", "lanplus", "-H", "10.0.0.1", "-U", "admin", "-P", "secretPassword123", "chassis", "power", "status"]
    masked = adapter._mask_password(cmd)
    
    # Assert secretPassword123 is masked
    assert "secretPassword123" not in masked
    assert "********" in masked
    # Assert other args remain visible
    assert "admin" in masked
    assert "10.0.0.1" in masked
    assert "-P" in masked
