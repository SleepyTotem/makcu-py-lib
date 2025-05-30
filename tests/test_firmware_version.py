# tests/test_firmware_version.py

def test_firmware_version(makcu):
    print("Getting firmware version...")
    version = makcu.mouse.get_firmware_version()
    print(f"Firmware version: {version}")
    assert version and len(version.strip()) > 0