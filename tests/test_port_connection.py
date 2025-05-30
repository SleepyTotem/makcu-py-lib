# test_port_connection.py

def test_port_connection(makcu):
    assert makcu.is_connected()