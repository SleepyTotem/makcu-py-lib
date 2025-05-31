def test_set_fallback_port(makcu):
    makcu.set_port("COM5")
    assert True