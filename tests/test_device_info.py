# tests/test_device_info.py

def test_device_info(makcu):
    print("Fetching device info...")
    info = makcu.mouse.get_device_info()
    print(f"Device Info: {info}")
    assert info.get("port")
    assert info.get("isConnected") is True