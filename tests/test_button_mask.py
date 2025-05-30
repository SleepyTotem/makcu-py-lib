# test_button_mask.py

def test_button_mask(makcu):
    print("Getting button mask...")
    mask = makcu.get_button_mask()
    print(f"Mask value: {mask}")
    assert isinstance(mask, int)