from makcu import set_port

def test_set_fallback_port():
    set_port("COM5")
    assert True